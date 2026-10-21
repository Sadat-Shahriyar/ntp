#!/usr/bin/env python3
"""
paper_extractor_ollama_textdump.py

Pipeline:
1. Preprocess + segment real-time systems / schedulability paper text.
2. Build focused prompts for each concept:
   - workload model
   - resource model
   - scheduler
   - analysis framework
   - invariants (lemmas/theorems)
3. Send those chunks to a local Ollama model (e.g. llama3.1:70b or deepseek-r1:32b).
4. Dump the model's free-form answers into .txt files.

No JSON. No parsing. Just straight text.

Requirements:
    pip install requests
Make sure Ollama is running locally.
"""

from __future__ import annotations
import re
import textwrap
from typing import List, Dict, Any, Optional
import requests
import os

# ============================================================
# 1. Ollama client
# ============================================================

class OllamaLLMClient:
    """
    Minimal client for talking to local Ollama.

    We'll send a single prompt string and get back the concatenated text
    from the streaming /api/generate endpoint.
    """

    def __init__(self, model_name: str = "llama3.1:70b", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host.rstrip("/")

    def _ollama_generate(self, prompt: str) -> str:
        """
        Call Ollama /api/generate (streaming) and return the full text.
        """
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "options": {
                "temperature": 0  # low temp => more extractive, less creative
            }
        }

        r = requests.post(url, json=payload, stream=True)
        r.raise_for_status()

        full = ""
        for line in r.iter_lines():
            if not line:
                continue
            data = line.decode("utf-8")
            try:
                data_json = __import__("json").loads(data)
            except Exception:
                continue
            if "response" in data_json:
                full += data_json["response"]
        return full.strip()

    # Prompt builders for each concept.
    # NOTE: We are *not* forcing JSON now. We just ask for structured prose.

    def build_workload_prompt(self, chunk_text: str) -> str:
        return textwrap.dedent(f"""
        Extract and clearly explain the WORKLOAD / TASK MODEL described below.

        Specifically summarize in plain text:
        - How tasks/jobs arrive (e.g., sporadic, periodic, etc.)
        - Parameters of each task (Ci, Di, Ti, utilization, density, dbf, etc.)
        - Any assumptions like constrained deadlines, implicit deadlines
        - Any additional timing constraints (jitter, offsets, etc.) if mentioned

        Write this as a technical summary for a verification engineer.
        Include equations in LaTeX if they appear.

        TEXT_START
        {chunk_text}
        TEXT_END
        """).strip()

    def build_resource_prompt(self, chunk_text: str) -> str:
        return textwrap.dedent(f"""
        Extract and describe the RESOURCE / PLATFORM MODEL from the text.

        Explain in plain text:
        - What kind of processor platform is assumed (uniprocessor? identical m-core? unit-capacity processors?)
        - Are tasks allowed to migrate between processors? If yes, under what rules?
        - Is scheduling preemptive or non-preemptive? Any overhead assumptions?
        - Any assumptions about clusters / partitioned scheduling / global scheduling / communication cost
        - Any assumptions about shared resources, locks, etc., if present.

        Write a clear summary suitable for formal modeling.

        TEXT_START
        {chunk_text}
        TEXT_END
        """).strip()

    def build_scheduler_prompt(self, chunk_text: str) -> str:
        return textwrap.dedent(f"""
        Extract and summarize the SCHEDULER.

        Explain in plain text:
        - The scheduling algorithm(s) (EDF, DM, FJP, FTP, global vs partitioned, etc.)
        - How priorities are assigned
        - How jobs are dispatched when multiple are ready
        - Preemption rules
        - Tie-breaking rules if discussed
        - Any mention of phenomena like the Dhall effect or special handling

        Present the answer as a coherent technical note, including any math/definitions.

        TEXT_START
        {chunk_text}
        TEXT_END
        """).strip()

    def build_analysis_prompt(self, analysis_text: str, equations_text: str) -> str:
        merged = analysis_text + "\n\n[KEY_EQUATIONS]\n" + equations_text
        return textwrap.dedent(f"""
        Summarize the SCHEDULABILITY ANALYSIS FRAMEWORK that the paper proposes or discusses.

        Include:
        - The style of analysis (e.g. demand bound function, interference/carry-in analysis,
          busy-window analysis, response-time analysis, density test, etc.)
        - The actual schedulability condition(s) and inequalities in math form
        - The meaning of parameters (A_k, D_k, C_k, m, etc.)
        - What must be checked to prove a task set is schedulable
        - Any statements about complexity (polynomial vs pseudo-polynomial)

        Keep the math statements and conditions explicit in LaTeX if possible.

        TEXT_START
        {merged}
        TEXT_END
        """).strip()

    def build_invariants_prompt(self, invariants_block: str) -> str:
        return textwrap.dedent(f"""
        From the text below, extract all system invariants / lemmas / theorems / corollaries
        that are stated as conditions that MUST hold for correctness or schedulability.

        For each lemma / theorem:
        - Give its name (e.g. "Lemma 1", "Theorem 2", etc.)
        - Restate the claim in your own words (plain English)
        - Copy any formal math statement or condition in LaTeX, if available
        - Explain informally WHY that invariant matters for schedulability
          (e.g. "this ensures no more than m-1 tasks contribute carry-in", etc.)

        Output should just be a readable list. Do NOT produce JSON.

        TEXT_START
        {invariants_block}
        TEXT_END
        """).strip()

    # Public helpers to actually run each prompt against Ollama

    def infer_workload_text(self, chunk_text: str) -> str:
        return self._ollama_generate(self.build_workload_prompt(chunk_text))

    def infer_resource_text(self, chunk_text: str) -> str:
        return self._ollama_generate(self.build_resource_prompt(chunk_text))

    def infer_scheduler_text(self, chunk_text: str) -> str:
        return self._ollama_generate(self.build_scheduler_prompt(chunk_text))

    def infer_analysis_text(self, analysis_text: str, equations_text: str) -> str:
        return self._ollama_generate(self.build_analysis_prompt(analysis_text, equations_text))

    def infer_invariants_text(self, invariants_block: str) -> str:
        return self._ollama_generate(self.build_invariants_prompt(invariants_block))


# ============================================================
# 2. Regex helpers for structure extraction
# ============================================================

SECTION_RE = re.compile(
    r'(?:^\\section\{(?P<sec_latex>.+?)\}\s*|'        # \section{...}
    r'^(?P<sec_md>#{1,3})\s+(?P<sec_md_title>.+)$)',   # # ..., ## ...
    flags=re.MULTILINE
)

SUBSECTION_RE = re.compile(
    r'(?:^\\subsection\{(?P<sub_latex>.+?)\}\s*|'     # \subsection{...}
    r'^(?P<sub_md>#{4,6})\s+(?P<sub_md_title>.+)$)',  # #### ...
    flags=re.MULTILINE
)

THEOREM_ENV_RE = re.compile(
    r'\\begin\{(?P<kind>theorem|lemma|claim|property|proposition|corollary|assumption|invariant)\}'
    r'(?P<body>.*?)'
    r'\\end\{\1\}',
    flags=re.IGNORECASE | re.DOTALL
)

INLINE_THEOREM_RE = re.compile(
    r'(\*\*(?P<kind2>(Lemma|Theorem|Corollary|Property|Claim)\s*\d*)\*\*\s*:?\s*'
    r'(?P<body2>.*?))'
    r'(?=(\n\s*\n|\r\n\r\n|\*\*(Lemma|Theorem|Corollary|Property|Claim)|^##|^\\section|$))',
    flags=re.IGNORECASE | re.DOTALL | re.MULTILINE
)

EQUATION_ENV_RE = re.compile(
    r'(\\begin\{equation\}.*?\\end\{equation\}'
    r'|\\\[.*?\\\]'
    r'|\$\$.*?\$\$)',
    flags=re.DOTALL
)

SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')


def normalize_whitespace(s: str) -> str:
    return re.sub(r'[ \t]+', ' ', s.replace('\r', '')).strip()


def extract_sections(text: str) -> List[Dict[str, Any]]:
    """
    Split text into top-level sections based on \section or markdown headers (#, ##, ###).
    Returns [{ "title": str, "content": str }, ...]
    """
    matches = list(SECTION_RE.finditer(text))
    if not matches:
        return [{"title": "FULL_DOCUMENT", "content": text}]

    sections: List[Dict[str, Any]] = []
    for i, m in enumerate(matches):
        title = m.group("sec_latex") or m.group("sec_md_title") or ""
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        sections.append({
            "title": normalize_whitespace(title),
            "content": body.strip()
        })
    return sections


def extract_subsections(section_text: str) -> List[Dict[str, Any]]:
    """
    Split section into subsections via \subsection or markdown (####, ##### ...).
    If none found, return the entire section as a single pseudo-subsection.
    """
    matches = list(SUBSECTION_RE.finditer(section_text))
    if not matches:
        return [{"title": "NO_SUBSECTIONS", "content": section_text.strip()}]

    result: List[Dict[str, Any]] = []
    for i, m in enumerate(matches):
        title = m.group("sub_latex") or m.group("sub_md_title") or ""
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section_text)
        body = section_text[start:end]
        result.append({
            "title": normalize_whitespace(title),
            "content": body.strip()
        })
    return result


def extract_equations(text: str) -> List[str]:
    """
    Grab display-style equations and keep them as LaTeX-ish strings.
    We'll pass them to the 'analysis' prompt.
    """
    equations: List[str] = []
    for m in EQUATION_ENV_RE.finditer(text):
        eq = m.group(0).strip()
        eq = re.sub(r'\s+', ' ', eq)
        equations.append(eq)
    return equations


def window_sentences(context: str, start_idx: int, end_idx: int, window: int = 3) -> str:
    """
    Take +/-window sentences around [start_idx:end_idx] so the LLM
    sees local meaning for lemmas/theorems.
    """
    sentences = []
    pos = 0
    for piece in SENTENCE_SPLIT_RE.split(context):
        piece = piece.strip()
        if not piece:
            continue
        start = context.find(piece, pos)
        end = start + len(piece)
        pos = end
        sentences.append((piece, start, end))

    idxs = [i for i, (_, s, e) in enumerate(sentences)
            if not (e < start_idx or s > end_idx)]
    if not idxs:
        return context[start_idx:end_idx]

    i0 = max(min(idxs) - window, 0)
    i1 = min(max(idxs) + window, len(sentences) - 1)
    selected = [sentences[i][0] for i in range(i0, i1 + 1)]
    return " ".join(selected).strip()


def extract_invariant_blocks(full_text: str) -> List[Dict[str, str]]:
    """
    Pull (Lemma|Theorem|Corollary|...) blocks in two formats:
      1. \\begin{lemma} ... \\end{lemma} (LaTeX style)
      2. **Lemma 1**: ... (Markdown-ish style)
    Attach nearby context so the model can interpret purpose.
    """
    blocks: List[Dict[str, str]] = []

    # LaTeX-style \begin{lemma}...\end{lemma}
    for m in THEOREM_ENV_RE.finditer(full_text):
        kind = m.group("kind")            # lemma / theorem / corollary ...
        body = m.group("body").strip()    # inside the env
        start_idx, end_idx = m.span()
        ctx = window_sentences(full_text, start_idx, end_idx, window=3)
        blocks.append({
            "label": kind.capitalize(),
            "body_with_context": f"{kind.upper()}:\n{body}\n\nLOCAL_CONTEXT:\n{ctx}"
        })

    # Markdown-style **Lemma 1**: ...
    for m in INLINE_THEOREM_RE.finditer(full_text):
        label = m.group("kind2").strip()  # e.g. "Lemma 1"
        body2 = m.group("body2").strip()
        start_idx, end_idx = m.span()
        ctx = window_sentences(full_text, start_idx, end_idx, window=3)
        blocks.append({
            "label": label,
            "body_with_context": f"{label}:\n{body2}\n\nLOCAL_CONTEXT:\n{ctx}"
        })

    return blocks


# ============================================================
# 3. Chunk classification by topic
# ============================================================

WORKLOAD_KEYWORDS = [
    "system model", "task model", "workload", "sporadic task",
    "task and system characteristics", "utilization", "density",
    "assumptions", "model"
]

RESOURCE_KEYWORDS = [
    "processor", "platform", "resource", "machine model",
    "multiprocessor", "identical processors", "unit-capacity",
    "migration", "execution model", "preemptive"
]

SCHEDULER_KEYWORDS = [
    "scheduler", "scheduling", "priority", "fixed job-priority", "fjp",
    "edf", "deadline monotonic", "dispatch", "tie-breaking", "dhall effect"
]

ANALYSIS_KEYWORDS = [
    "schedulability", "analysis", "schedulability test",
    "worst-case behavior",
    "global edf schedulability", "improved schedulability algorithm",
    "theorem", "condition", "equation", "corollary",
    "proof sketch", "corollary"
]


def section_matches_keywords(title: str, keywords: List[str]) -> bool:
    lower_title = title.lower()
    return any(kw.lower() in lower_title for kw in keywords)


def classify_subsections(sections: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Bucket text into {workload, resource, scheduler, analysis}
    by matching keywords on section/subsection titles.
    """
    buckets = {
        "workload": [],
        "resource": [],
        "scheduler": [],
        "analysis": [],
    }

    for sec in sections:
        sec_title = sec["title"]
        subsections = extract_subsections(sec["content"])

        # first pass: look at subsections
        for sub in subsections:
            sub_title = sub["title"]
            block_text = sub["content"]
            combo_title = f"{sec_title} / {sub_title}"

            if section_matches_keywords(combo_title, WORKLOAD_KEYWORDS):
                buckets["workload"].append(block_text)

            if section_matches_keywords(combo_title, RESOURCE_KEYWORDS):
                buckets["resource"].append(block_text)

            if section_matches_keywords(combo_title, SCHEDULER_KEYWORDS):
                buckets["scheduler"].append(block_text)

            if section_matches_keywords(combo_title, ANALYSIS_KEYWORDS):
                buckets["analysis"].append(block_text)

        # also treat the entire section as a candidate
        if section_matches_keywords(sec_title, WORKLOAD_KEYWORDS):
            buckets["workload"].append(sec["content"])

        if section_matches_keywords(sec_title, RESOURCE_KEYWORDS):
            buckets["resource"].append(sec["content"])

        if section_matches_keywords(sec_title, SCHEDULER_KEYWORDS):
            buckets["scheduler"].append(sec["content"])

        if section_matches_keywords(sec_title, ANALYSIS_KEYWORDS):
            buckets["analysis"].append(sec["content"])

    # Deduplicate
    for k in buckets:
        seen = set()
        deduped = []
        for blk in buckets[k]:
            norm = blk.strip()
            if norm and norm not in seen:
                deduped.append(norm)
                seen.add(norm)
        buckets[k] = deduped

    return buckets


def join_with_headers(blocks: List[str], header: str) -> str:
    """
    Concatenate blocks with markers to give Ollama context but preserve boundaries.
    """
    if not blocks:
        return ""
    pieces = []
    for i, b in enumerate(blocks):
        pieces.append(
            f"=== {header} CHUNK {i} START ===\n{b.strip()}\n=== {header} CHUNK {i} END ==="
        )
    return "\n\n".join(pieces)


def build_invariants_blob(invariant_blocks: List[Dict[str, str]]) -> str:
    """
    Stitch together all lemma/theorem/etc. contexts into a single big block.
    """
    parts = []
    for i, blk in enumerate(invariant_blocks):
        label = blk["label"]
        body_ctx = blk["body_with_context"]
        parts.append(
            f"=== INVARIANT {i} : {label} START ===\n{body_ctx}\n=== INVARIANT {i} END ==="
        )
    return "\n\n".join(parts)


# ============================================================
# 4. Top-level orchestrator
# ============================================================

class PaperExtractor:
    """
    Full pipeline from raw paper text -> 5 .txt files with model summaries.
    """

    def __init__(self,
                 llm: Optional[OllamaLLMClient] = None,
                 model_name: str = "llama3.1:70b",
                 host: str = "http://localhost:11434"):
        if llm is None:
            llm = OllamaLLMClient(model_name=model_name, host=host)
        self.llm = llm

    def preprocess(self, raw_text: str) -> Dict[str, Any]:
        """
        Extract sections, equations, invariants from the raw LaTeX/markdown-ish text.
        """
        sections = extract_sections(raw_text)
        equations = extract_equations(raw_text)
        invariant_blocks = extract_invariant_blocks(raw_text)
        return {
            "sections": sections,
            "equations": equations,
            "invariant_blocks": invariant_blocks,
        }

    def run(self, raw_text: str, out_dir: str = ".") -> Dict[str, str]:
        """
        Main entry point you call.

        Steps:
        - preprocess & segment
        - make semantic chunks
        - ask LLM 5 questions
        - write answers to disk in out_dir

        Returns dict of file paths written.
        """
        os.makedirs(out_dir, exist_ok=True)

        # --- 1. preprocess
        pre = self.preprocess(raw_text)
        sections = pre["sections"]
        equations = pre["equations"]
        invariant_blocks = pre["invariant_blocks"]

        # --- 2. bucket into semantic chunks
        buckets = classify_subsections(sections)
        workload_blob  = join_with_headers(buckets["workload"],  "WORKLOAD")
        resource_blob  = join_with_headers(buckets["resource"],  "RESOURCE")
        scheduler_blob = join_with_headers(buckets["scheduler"], "SCHEDULER")
        analysis_blob  = join_with_headers(buckets["analysis"],  "ANALYSIS")
        invariants_blob = build_invariants_blob(invariant_blocks)

        # Prepare equations blob just for analysis
        eq_text = ""
        if equations:
            eq_text = "\n".join([f"[EQ{i}] {eq}" for i, eq in enumerate(equations)])

        # --- 3. ask the model for each part (skip empty chunks gracefully)

        workload_answer = ""
        if workload_blob.strip():
            workload_answer = self.llm.infer_workload_text(workload_blob)
        else:
            workload_answer = "No workload/task model section detected by heuristic."

        resource_answer = ""
        if resource_blob.strip():
            resource_answer = self.llm.infer_resource_text(resource_blob)
        else:
            resource_answer = "No resource/platform model section detected by heuristic."

        scheduler_answer = ""
        if scheduler_blob.strip():
            scheduler_answer = self.llm.infer_scheduler_text(scheduler_blob)
        else:
            scheduler_answer = "No scheduler/policy section detected by heuristic."

        analysis_answer = ""
        if analysis_blob.strip():
            analysis_answer = self.llm.infer_analysis_text(analysis_blob, eq_text)
        else:
            analysis_answer = "No schedulability analysis section detected by heuristic."

        invariants_answer = ""
        if invariants_blob.strip():
            invariants_answer = self.llm.infer_invariants_text(invariants_blob)
        else:
            invariants_answer = "No lemmas/theorems detected by heuristic."

        # --- 4. write to files
        out_files = {
            "workload_model":       os.path.join(out_dir, "workload_model.txt"),
            "resource_model":       os.path.join(out_dir, "resource_model.txt"),
            "scheduler":            os.path.join(out_dir, "scheduler.txt"),
            "analysis_framework":   os.path.join(out_dir, "analysis_framework.txt"),
            "invariants":           os.path.join(out_dir, "invariants.txt"),
        }

        with open(out_files["workload_model"], "w", encoding="utf-8") as f:
            f.write(workload_answer)

        with open(out_files["resource_model"], "w", encoding="utf-8") as f:
            f.write(resource_answer)

        with open(out_files["scheduler"], "w", encoding="utf-8") as f:
            f.write(scheduler_answer)

        with open(out_files["analysis_framework"], "w", encoding="utf-8") as f:
            f.write(analysis_answer)

        with open(out_files["invariants"], "w", encoding="utf-8") as f:
            f.write(invariants_answer)

        return out_files


# ============================================================
# 5. DEMO / HOW TO RUN
# ============================================================

FULL_PAPER_TEXT = r"""
# Techniques for Multiprocessor Global Schedulability Analysis+
Sanjoy Baruah

## 2 Model

A sporadic task \(\tau_{i}=(C_{i},D_{i},T_{i})\) is characterized by a worst-case execution requirement \(C_{i}\),
a (relative) deadline \(D_{i}\), and a minimum inter-arrival separation \(T_{i}\) (also called the period).
We consider systems of sporadic tasks executing on several identical processors.
We assume fully preemptive execution: any job can be interrupted at any time and resumed later at no cost.
Global scheduling allows migration of jobs between processors; partitioned scheduling binds each task to one processor.
We restrict attention to constrained-deadline and implicit-deadline systems (D_i ≤ T_i).

Task and system characteristics.
Utilization u_i = C_i / T_i. Total utilization u_sum(τ) = Σ u_i.
Density δ_i = C_i / D_i; total density δ_sum(τ) = Σ δ_i.
Demand bound function dbf(τ_i, t) = floor((t - D_i)/T_i + 1) * C_i if t > D_i, else 0.

Fixed job-priority (FJP) scheduling:
Each job keeps a fixed priority from release until completion (though different jobs of same task can have different priorities).
EDF assigns higher priority to jobs with earlier deadlines.
Global EDF can suffer from the Dhall effect, so hybrid schemes sometimes give certain tasks highest priority.

## 4 Partitioned versus global FJP scheduling

**Lemma 1**: There are task systems schedulable by global FJP that partitioned FJP cannot schedule.
**Lemma 2**: There are task systems schedulable by partitioned FJP that global FJP cannot schedule.
**Theorem 1**: Therefore, global and partitioned FJP scheduling are incomparable.

## 5 Global edf schedulability: Prior results

Known tests:
- Density test: δ_sum(τ) ≤ m - (m-1) δ_max(τ)
- Baker's [bak] test: reason about carry-in and denial of service to τ_k.
- Bertogna/Cirinei/Lipari [bcl] test: similar but simpler bounds.
These tests differ in how they bound interference and carry-in work.

## 6 An improved schedulability algorithm

Define A_k as the time since last idle instant before τ_k's arrival.
Let I1(τ_i) and I2(τ_i) bound each task's contribution in an interference window.
At most (m-1) tasks can carry-in extra work at that instant.

**Theorem 2**: τ is EDF-schedulable on m processors if, for each task τ_k and all A_k ≥ 0,
sum(I1(τ_i)) + sum_{(m-1) largest} (I2(τ_i) - I1(τ_i)) ≤ m(A_k + D_k - C_k).
This generalizes the uniprocessor exact EDF schedulability test (Corollary 1),
and runs in pseudo-polynomial time (Theorem 3 / Corollary 2).
"""

from input_text import input_text

FULL_PAPER_TEXT = input_text

def main():
    # configure model here
    extractor = PaperExtractor(
        model_name="llama3.1:70b",          # change to your ollama model tag
        host="http://localhost:11434",      # change if Ollama not default
    )

    output_paths = extractor.run(
        raw_text=FULL_PAPER_TEXT,
        out_dir="extraction_outputs"        # results will be written here
    )

    print("Extraction finished. Wrote:")
    for name, path in output_paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
