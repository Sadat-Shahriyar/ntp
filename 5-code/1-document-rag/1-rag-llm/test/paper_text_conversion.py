#!/usr/bin/env python3
"""
paper_extractor.py

Pipeline for extracting:
  - Workload model
  - Resource model
  - Scheduler
  - Analysis framework
  - System invariants (lemmas/theorems)

from real-time scheduling / schedulability analysis papers that have been OCR'd
or converted to LaTeX-like / markdown-like text (e.g. via Nougat).

High-level flow:
1. Preprocess & tag structure (sections, subsections, theorem-like blocks, equations)
2. Build semantic chunks for each concept of interest
3. Build focused prompts for each chunk so an LLM can emit strict JSON
4. (Optional) call your LLM and parse results

This file is written so you can:
- Run `python3 paper_extractor.py` to see demo prompts on the provided example text.
- Import `PaperExtractor` in other code and feed arbitrary papers.

You still need to:
- Implement LLMClient.generate_json() for your specific model API.
- Potentially tune regex keyword lists for your corpus.

Author: you :)
"""

from __future__ import annotations
import re
import json
import textwrap
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple


# ------------------------------------------------------------
# 0. Data models for structured output
# ------------------------------------------------------------

@dataclass
class WorkloadModel:
    task_arrival_model: str
    task_parameters: Dict[str, str]
    criticality_or_type: str
    additional_constraints: str
    confidence: str = "medium"


@dataclass
class ResourceModel:
    processing_platform: str
    migration_policy: str
    preemption_policy: str
    shared_resources: str
    additional_assumptions: str
    confidence: str = "medium"


@dataclass
class SchedulerModel:
    policy_name: str
    priority_assignment_rule: str
    dispatch_rule: str
    preemption_rule: str
    tie_breaking_rule: str
    confidence: str = "medium"


@dataclass
class AnalysisFramework:
    analysis_type: str
    key_equations: List[str]
    assumptions_required: str
    schedulability_test_statement: str
    confidence: str = "medium"


@dataclass
class Invariant:
    name: str
    statement: str
    informal_meaning: str
    scope: str
    confidence: str = "medium"


# ------------------------------------------------------------
# 1. Lightweight LLM client stub
# ------------------------------------------------------------

class LLMClient:
    """
    Stub interface you can plug your model API into.
    You want `generate_json(role_prompt, chunk_text)` to return a Python object.

    Example usage in real code:
      my_llm = LLMClient(...)
      result = my_llm.extract_workload(chunk_text)

    For now, methods just build prompt strings and (optionally) could call out.
    We'll keep them as stubs returning the prompt so you can inspect.
    """

    def __init__(self):
        pass

    def build_prompt(self, instruction: str, chunk_text: str) -> str:
        """
        Build a single text prompt that you can send as the 'user' message
        to a JSON-capable model (DeepSeek-R1, Llama 3.1, etc.)
        """
        prompt = textwrap.dedent(f"""
        {instruction}

        TEXT_START
        {chunk_text}
        TEXT_END
        """).strip()
        return prompt

    # Below: helper "prompt builders" for each concept.
    # You can either (a) just retrieve these prompts and send them manually,
    # or (b) extend to actually call your model and parse JSON.

    def prompt_for_workload(self, chunk_text: str) -> str:
        instruction = """
        You are extracting formal modeling assumptions for real-time task sets.
        Return ONLY valid MINIFIED JSON with keys:
        {
          "task_arrival_model": "...",
          "task_parameters": { "Ci": "...", "Di": "...", "Ti": "...", ... },
          "criticality_or_type": "...",
          "additional_constraints": "...",
          "confidence": "high|medium|low"
        }
        Only use information present in the text. Do not invent.
        """
        return self.build_prompt(instruction, chunk_text)

    def prompt_for_resource(self, chunk_text: str) -> str:
        instruction = """
        Extract the resource model for the described real-time system.
        Return ONLY valid MINIFIED JSON with keys:
        {
          "processing_platform": "...",   // e.g. uniprocessor, identical m-core
          "migration_policy": "...",      // e.g. global, partitioned, clustered
          "preemption_policy": "...",     // e.g. fully preemptive, non-preemptive
          "shared_resources": "...",      // locking / shared buses / etc.
          "additional_assumptions": "...",
          "confidence": "high|medium|low"
        }
        Only use information present in the text. Do not invent.
        """
        return self.build_prompt(instruction, chunk_text)

    def prompt_for_scheduler(self, chunk_text: str) -> str:
        instruction = """
        Summarize the scheduling policy.
        Return ONLY valid MINIFIED JSON with keys:
        {
          "policy_name": "...",                 // e.g. EDF, DM, FJP, etc.
          "priority_assignment_rule": "...",    // how priorities are chosen
          "dispatch_rule": "...",               // which job runs if multiple ready
          "preemption_rule": "...",             // when preemption happens
          "tie_breaking_rule": "...",           // if mentioned
          "confidence": "high|medium|low"
        }
        Only use information present in the text. Do not invent.
        """
        return self.build_prompt(instruction, chunk_text)

    def prompt_for_analysis(self, chunk_text: str, equations_text: str) -> str:
        """
        We also pass in explicitly extracted equations to encourage the LLM
        to surface them.
        """
        merged_chunk = chunk_text + "\n\nKEY_EQUATIONS_BLOCK:\n" + equations_text
        instruction = """
        Extract the schedulability analysis framework.
        Return ONLY valid MINIFIED JSON with keys:
        {
          "analysis_type": "...",
          "key_equations": ["...", "..."],       // verbatim LaTeX if short
          "assumptions_required": "...",
          "schedulability_test_statement": "...",
          "confidence": "high|medium|low"
        }
        Only use information present in the text. Do not invent.
        """
        return self.build_prompt(instruction, merged_chunk)

    def prompt_for_invariants(self, invariants_block: str) -> str:
        instruction = """
        You are extracting invariants that the scheduler relies on.
        For EACH lemma/theorem/property/etc in the text, output an OBJECT.
        Return ONLY valid MINIFIED JSON like:
        [
          {
            "name": "Theorem 1",
            "statement": "... full mathematical statement in LaTeX or text ...",
            "informal_meaning": "... why it matters for schedulability ...",
            "scope": "task|processor|system|interval",
            "confidence": "high|medium|low"
          },
          {
            "name": "Lemma 2",
            "statement": "...",
            "informal_meaning": "...",
            "scope": "...",
            "confidence": "..."
          }
        ]
        Only use information present in the text. Do not invent.
        """
        return self.build_prompt(instruction, invariants_block)


# ------------------------------------------------------------
# 2. Helpers for tagging and segmentation
# ------------------------------------------------------------

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

# Matches theorem-like LaTeX envs:
THEOREM_ENV_RE = re.compile(
    r'\\begin\{(?P<kind>theorem|lemma|claim|property|proposition|corollary|assumption|invariant)\}'
    r'(?P<body>.*?)'
    r'\\end\{\1\}',
    flags=re.IGNORECASE | re.DOTALL
)

# Matches markdown-ish inline Lemma/Theorem blocks like:
# **Lemma 1**: ... until blank line or next **Theorem**
INLINE_THEOREM_RE = re.compile(
    r'(\*\*(?P<kind2>(Lemma|Theorem|Corollary|Property|Claim)\s*\d*)\*\*\s*:?\s*'
    r'(?P<body2>.*?))'
    r'(?=(\n\s*\n|\r\n\r\n|\*\*(Lemma|Theorem|Corollary|Property|Claim)|^##|^\\section|$))',
    flags=re.IGNORECASE | re.DOTALL | re.MULTILINE
)

# Equation blocks (\begin{equation}...\end{equation}, \[...\], $$...$$)
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
    Rough section splitter.
    Returns a list of dicts: { "title": str, "content": str }
    Uses \section / markdown # as anchors.
    """
    # We'll find all top-level section headers and slice.
    matches = list(SECTION_RE.finditer(text))
    sections = []
    if not matches:
        # whole doc as one section
        return [{"title": "FULL_DOCUMENT", "content": text}]

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
    Split a section's body into subsections using \subsection / markdown ####.
    Returns [{ "title": str, "content": str }, ...]
    If none found, return entire section as a single pseudo-subsection.
    """
    matches = list(SUBSECTION_RE.finditer(section_text))
    if not matches:
        return [{"title": "NO_SUBSECTIONS", "content": section_text.strip()}]

    result = []
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
    Grab all top-level display-style equations we can spot.
    We'll keep LaTeX-ish content as-is to feed into analysis extraction.
    """
    eqs = []
    for m in EQUATION_ENV_RE.finditer(text):
        eq = m.group(0).strip()
        # compress whitespace but preserve math formatting around \, $, etc.
        eq = re.sub(r'\s+', ' ', eq)
        eqs.append(eq)
    return eqs


def window_sentences(context: str, start_idx: int, end_idx: int, window: int = 3) -> str:
    """
    Grab +/- 'window' sentences around a span [start_idx:end_idx] in `context`.
    Super simple sentence splitting heuristic.
    """
    # Split context into sentences with offsets
    # We'll walk and store (sentence_text, start, end)
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

    # find which sentence(s) intersect [start_idx,end_idx]
    idxs = [i for i, (_, s, e) in enumerate(sentences) if not (e < start_idx or s > end_idx)]
    if not idxs:
        return context[start_idx:end_idx]

    i0 = max(min(idxs) - window, 0)
    i1 = min(max(idxs) + window, len(sentences) - 1)

    selected = [sentences[i][0] for i in range(i0, i1 + 1)]
    return " ".join(selected).strip()


def extract_invariant_blocks(full_text: str) -> List[Dict[str, str]]:
    """
    Pull out Theorem/Lemma/etc. blocks in two ways:
      (1) LaTeX envs (\begin{theorem}...\end{theorem})
      (2) Markdown-ish **Lemma 1**: ...
    For each match, include local context (+/-3 sentences) to help the LLM infer informal meaning.
    Returns list of dicts { "label": "...", "body_with_context": "..." }
    """
    blocks: List[Dict[str, str]] = []

    # First: LaTeX-style environments
    for m in THEOREM_ENV_RE.finditer(full_text):
        kind = m.group("kind")
        body = m.group("body").strip()
        start_idx, end_idx = m.span()
        ctx = window_sentences(full_text, start_idx, end_idx, window=3)
        label_guess = kind.capitalize()
        blocks.append({
            "label": label_guess,
            "body_with_context": f"{kind.upper()}:\n{body}\n\nLOCAL_CONTEXT:\n{ctx}"
        })

    # Second: Markdown-style inline "**Lemma 1**: ..."
    for m in INLINE_THEOREM_RE.finditer(full_text):
        kind2 = m.group("kind2").strip()
        body2 = m.group("body2").strip()
        start_idx, end_idx = m.span()
        ctx = window_sentences(full_text, start_idx, end_idx, window=3)
        blocks.append({
            "label": kind2,
            "body_with_context": f"{kind2}:\n{body2}\n\nLOCAL_CONTEXT:\n{ctx}"
        })

    return blocks


# ------------------------------------------------------------
# 3. Chunking logic
# ------------------------------------------------------------

WORKLOAD_KEYWORDS = [
    "System Model", "Task Model", "Workload", "Model", "Sporadic task",
    "Task and system characteristics", "Utilization", "Density", "Assumptions"
]

RESOURCE_KEYWORDS = [
    "Processor", "Platform", "Resource", "Multiprocessor", "machine model",
    "identical processors", "unit-capacity processors", "migration",
    "preemptive execution model"
]

SCHEDULER_KEYWORDS = [
    "Scheduler", "Scheduling", "Priority", "fixed job-priority", "FJP",
    "edf", "deadline monotonic", "Dispatch", "tie-breaking"
]

ANALYSIS_KEYWORDS = [
    "Schedulability", "Analysis", "Schedulability test", "Worst-case behavior",
    "Global edf schedulability", "An improved schedulability algorithm",
    "Theorem", "Condition", "Equation"
]


def section_matches_keywords(title: str, keywords: List[str]) -> bool:
    t_lower = title.lower()
    return any(k.lower() in t_lower for k in keywords)


def classify_subsections(
    sections: List[Dict[str, Any]]
) -> Dict[str, List[str]]:
    """
    Given all top-level sections, split text into semantic buckets:
      workload_chunks, resource_chunks, scheduler_chunks, analysis_chunks

    We'll use title heuristics at both section and subsection level.
    Returns dict of lists of chunk strings.
    """
    buckets = {
        "workload": [],
        "resource": [],
        "scheduler": [],
        "analysis": [],
    }

    for sec in sections:
        sec_title = sec["title"]
        subs = extract_subsections(sec["content"])

        # if no_subsections, subs = [ {"title":"NO_SUBSECTIONS", "content":...} ]
        for sub in subs:
            sub_title = sub["title"]
            block_text = sub["content"]

            title_for_match = f"{sec_title} / {sub_title}"

            if section_matches_keywords(title_for_match, WORKLOAD_KEYWORDS):
                buckets["workload"].append(block_text)

            if section_matches_keywords(title_for_match, RESOURCE_KEYWORDS):
                buckets["resource"].append(block_text)

            if section_matches_keywords(title_for_match, SCHEDULER_KEYWORDS):
                buckets["scheduler"].append(block_text)

            if section_matches_keywords(title_for_match, ANALYSIS_KEYWORDS):
                buckets["analysis"].append(block_text)

        # also consider the entire section as fallback
        if section_matches_keywords(sec_title, WORKLOAD_KEYWORDS):
            buckets["workload"].append(sec["content"])
        if section_matches_keywords(sec_title, RESOURCE_KEYWORDS):
            buckets["resource"].append(sec["content"])
        if section_matches_keywords(sec_title, SCHEDULER_KEYWORDS):
            buckets["scheduler"].append(sec["content"])
        if section_matches_keywords(sec_title, ANALYSIS_KEYWORDS):
            buckets["analysis"].append(sec["content"])

    # Deduplicate by simple string uniq
    for k in buckets:
        deduped = []
        seen = set()
        for blk in buckets[k]:
            blk_norm = blk.strip()
            if blk_norm and blk_norm not in seen:
                deduped.append(blk_norm)
                seen.add(blk_norm)
        buckets[k] = deduped

    return buckets


def join_with_headers(blocks: List[str], header: str) -> str:
    """
    If we have multiple relevant chunks, concatenate them with markers.
    """
    if not blocks:
        return ""
    out_parts = []
    for i, b in enumerate(blocks):
        out_parts.append(f"=== {header} CHUNK {i} START ===\n{b.strip()}\n=== {header} CHUNK {i} END ===")
    return "\n\n".join(out_parts)


# ------------------------------------------------------------
# 4. Orchestrator
# ------------------------------------------------------------

class PaperExtractor:
    """
    High-level driver:
      - feed raw text
      - produce structured prompts for each extraction task
      - (optionally) call llm to get JSON, then parse to dataclasses
    """

    def __init__(self, llm: Optional[LLMClient] = None):
        self.llm = llm if llm is not None else LLMClient()

    def preprocess(self, raw_text: str) -> Dict[str, Any]:
        """
        Tag & segment: sections, equations, invariants, etc.
        Returns dict with:
          sections
          equations
          invariant_blocks
        """
        sections = extract_sections(raw_text)
        equations = extract_equations(raw_text)
        invariant_blocks = extract_invariant_blocks(raw_text)

        return {
            "sections": sections,
            "equations": equations,
            "invariant_blocks": invariant_blocks,
        }

    def build_semantic_chunks(self, sections: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Run classification heuristics and return big concatenated text blobs
        per concept.
        """
        buckets = classify_subsections(sections)

        workload_blob  = join_with_headers(buckets["workload"],  "WORKLOAD")
        resource_blob  = join_with_headers(buckets["resource"],  "RESOURCE")
        scheduler_blob = join_with_headers(buckets["scheduler"], "SCHEDULER")
        analysis_blob  = join_with_headers(buckets["analysis"],  "ANALYSIS")

        return {
            "workload_blob": workload_blob,
            "resource_blob": resource_blob,
            "scheduler_blob": scheduler_blob,
            "analysis_blob": analysis_blob,
        }

    def build_invariants_blob(self, invariant_blocks: List[Dict[str, str]]) -> str:
        """
        Concatenate all lemma/theorem-like chunks + local context nearby.
        """
        parts = []
        for i, blk in enumerate(invariant_blocks):
            label = blk["label"]
            body_ctx = blk["body_with_context"]
            parts.append(f"=== INVARIANT {i} : {label} START ===\n{body_ctx}\n=== INVARIANT {i} END ===")
        return "\n\n".join(parts)

    # -- PROMPT BUILDING ------------------------------------------------

    def build_workload_prompt(self, workload_blob: str) -> str:
        return self.llm.prompt_for_workload(workload_blob)

    def build_resource_prompt(self, resource_blob: str) -> str:
        return self.llm.prompt_for_resource(resource_blob)

    def build_scheduler_prompt(self, scheduler_blob: str) -> str:
        return self.llm.prompt_for_scheduler(scheduler_blob)

    def build_analysis_prompt(self, analysis_blob: str, equations: List[str]) -> str:
        eq_text = "\n".join([f"[EQ{i}] {eq}" for i, eq in enumerate(equations)])
        return self.llm.prompt_for_analysis(analysis_blob, eq_text)

    def build_invariants_prompt(self, invariants_blob: str) -> str:
        return self.llm.prompt_for_invariants(invariants_blob)

    # -- (OPTIONAL) PARSERS --------------------------------------------
    # After you actually run the prompts through your model, you'll get JSON back.
    # You can parse them into the dataclasses defined above.

    def parse_workload_json(self, json_str: str) -> WorkloadModel:
        data = json.loads(json_str)
        return WorkloadModel(
            task_arrival_model=data.get("task_arrival_model", ""),
            task_parameters=data.get("task_parameters", {}),
            criticality_or_type=data.get("criticality_or_type", ""),
            additional_constraints=data.get("additional_constraints", ""),
            confidence=data.get("confidence", "medium")
        )

    def parse_resource_json(self, json_str: str) -> ResourceModel:
        data = json.loads(json_str)
        return ResourceModel(
            processing_platform=data.get("processing_platform", ""),
            migration_policy=data.get("migration_policy", ""),
            preemption_policy=data.get("preemption_policy", ""),
            shared_resources=data.get("shared_resources", ""),
            additional_assumptions=data.get("additional_assumptions", ""),
            confidence=data.get("confidence", "medium"),
        )

    def parse_scheduler_json(self, json_str: str) -> SchedulerModel:
        data = json.loads(json_str)
        return SchedulerModel(
            policy_name=data.get("policy_name", ""),
            priority_assignment_rule=data.get("priority_assignment_rule", ""),
            dispatch_rule=data.get("dispatch_rule", ""),
            preemption_rule=data.get("preemption_rule", ""),
            tie_breaking_rule=data.get("tie_breaking_rule", ""),
            confidence=data.get("confidence", "medium"),
        )

    def parse_analysis_json(self, json_str: str) -> AnalysisFramework:
        data = json.loads(json_str)
        return AnalysisFramework(
            analysis_type=data.get("analysis_type", ""),
            key_equations=data.get("key_equations", []),
            assumptions_required=data.get("assumptions_required", ""),
            schedulability_test_statement=data.get("schedulability_test_statement", ""),
            confidence=data.get("confidence", "medium"),
        )

    def parse_invariants_json(self, json_str: str) -> List[Invariant]:
        arr = json.loads(json_str)
        out: List[Invariant] = []
        for obj in arr:
            out.append(Invariant(
                name=obj.get("name", ""),
                statement=obj.get("statement", ""),
                informal_meaning=obj.get("informal_meaning", ""),
                scope=obj.get("scope", ""),
                confidence=obj.get("confidence", "medium"),
            ))
        return out


# ------------------------------------------------------------
# 5. Demonstration using the text you gave
# ------------------------------------------------------------

DEMO_TEXT = r"""
# Techniques for Multiprocessor Global Schedulability Analysis+
Footnote †: Supported in part by NSF Grant Nos. CNS-0408996, CCF-0541056, and CCR-0615197, ARO Grant No. W911NF-06-1-0425, and funding from the Intel Corporation.

Sanjoy Baruah

The University of North Carolina at Chapel Hill

###### Abstract

The scheduling of sporadic task systems upon multiprocessor platforms is considered, when inter-processor migration is permitted. It is known that current schedulability tests for such systems perform quite poorly when compared to schedulability tests for partitioned scheduling. Limitations of current tests are identified, which may be responsible for the unsatisfactory performance of these tests. A new test that overcomes some of these limitations is proposed and proved correct.

## 1 Introduction and Motivation

A real-time system is often modelled as a finite collection of independent recurring tasks, each of which generates a potentially infinite sequence of jobs. Every job is characterized by an arrival time, an execution requirement, and a deadline, and it is required that a job complete execution between its arrival time and its deadline. Different formal models for recurring tasks place different restrictions on the values of the parameters of jobs generated by each task. One of the more commonly used formal models is the sporadic task model[23, 9], which will be considered in this paper.

Scheduling is the allocation of processor time to jobs, and a scheduling algorithm is used for determining such allocation. A schedulability test for a given scheduling algorithm accepts as input the specifications of a real-time system, and determines whether the scheduling algorithm can guarantee to schedule the system such that all jobs of all tasks will meet all deadlines, under all permissible combinations of job-arrival sequences by the different tasks comprising the system. In this paper, we study the scheduling of systems of sporadic tasks upon a platform comprised of several identical processors. In scheduling a task system upon such a platform, it is possible to divide the processors into clusters and assign each task to a cluster...

## 2 Model

A sporadic task \\(\\tau_{i}=(C_{i},D_{i},T_{i})\\) is characterized by a worst-case execution requirement \\(C_{i}\\), a (relative) deadline \\(D_{i}\\), and a minimum inter-arrival separation \\(T_{i}\\)...

We assume a fully preemptive execution model...
... partitioned vs global scheduling ...
Fixed job-priority (FJP) scheduling...
It has long been known that global edf ... Dhall effect ...

## 3 Global scheduling and Worst-case behavior

Recall that in order for a sporadic task system to be considered A-schedulable ...
**Example 1**: Consider the task system comprised of the three tasks ...

## 4 Partitioned versus global FJP scheduling

**Lemma 1**: There are task systems that are schedulable using global FJP algorithms that partitioned FJP algorithms cannot schedule.
**Proof Sketch:** Here's an example task system, on \\(2\\) processors:
\\[\\tau_{1}=(2,2,3),\\tau_{2}=(3,3,4),\\tau_{3}=(5,12,12)\\]

**Lemma 2**: There are task systems that are schedulable using partitioned FJP algorithms that global FJP algorithms cannot schedule.
...
**Theorem 1**: Global and partitioned FJP scheduling are incomparable.

## 5 Global edf schedulability: Prior results

The density, [bak], and [bcl] tests...
Equation (1): \\(\\delta_{\\mathrm{sum}}(\\tau) \\leq m-(m-1)\\delta_{\\mathrm{max}}(\\tau)\\).

## 6 An improved schedulability algorithm

We have designed a new global edf-schedulability test...
It will be shown (Corollary 1) that our test generalizes the known exact edf-schedulability test on uniprocessors.
Equation (2): \\sum I(\\tau_i) > m(A_k + D_k - C_k)
Equation (8): sufficiency condition...

**Theorem 2**: Task system \\tau is edf-schedulable upon m unit-capacity processors if ...
**Corollary 1**: The edf schedulability test of Theorem 2 is a generalization...
**Theorem 3**: If Condition 8 is to be violated...
**Corollary 2**: The condition in Theorem 2 above can be tested ...

## 7 Conclusions
...
"""

from input_text import input_text

DEMO_TEXT = input_text

def demo():
    print("=== DEMO: running extractor on provided paper text ===\n")

    extractor = PaperExtractor()

    # Step 1: preprocess structure
    pre = extractor.preprocess(DEMO_TEXT)
    sections = pre["sections"]
    equations = pre["equations"]
    invariant_blocks = pre["invariant_blocks"]

    # Step 2: semantic chunks
    chunks = extractor.build_semantic_chunks(sections)
    workload_blob  = chunks["workload_blob"]
    resource_blob  = chunks["resource_blob"]
    scheduler_blob = chunks["scheduler_blob"]
    analysis_blob  = chunks["analysis_blob"]

    invariants_blob = extractor.build_invariants_blob(invariant_blocks)

    # Step 3: build prompts
    workload_prompt   = extractor.build_workload_prompt(workload_blob)
    resource_prompt   = extractor.build_resource_prompt(resource_blob)
    scheduler_prompt  = extractor.build_scheduler_prompt(scheduler_blob)
    analysis_prompt   = extractor.build_analysis_prompt(analysis_blob, equations)
    invariants_prompt = extractor.build_invariants_prompt(invariants_blob)

    # Show the prompts you'd actually send to the LLM.
    print("\n--- WORKLOAD PROMPT ---\n")
    print(workload_prompt)

    print("\n--- RESOURCE PROMPT ---\n")
    print(resource_prompt)

    print("\n--- SCHEDULER PROMPT ---\n")
    print(scheduler_prompt)

    print("\n--- ANALYSIS PROMPT ---\n")
    print(analysis_prompt)

    print("\n--- INVARIANTS PROMPT ---\n")
    print(invariants_prompt)

    print("\n=== END DEMO ===")


if __name__ == "__main__":
    demo()
