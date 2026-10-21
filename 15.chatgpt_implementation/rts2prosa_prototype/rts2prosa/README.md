# RTS2Prosa prototype

This repository implements the fixed architecture:

```text
RTS PAPER / MARKDOWN
  -> Document / Theory Graph
  -> ModelIR
  -> AnalysisIR
  -> ProofIR
  -> Prosa Semantic Matcher
       EXACT MATCH / COMPOSITIONAL MATCH / NO MATCH / INSUFFICIENT SOURCE
       NO MATCH -> explicit Prosa extension specification
  -> ProsaIR
  -> Rocq Skeleton
  -> Proof Completion
  -> Rocq Verification + repair loop
  -> Semantic-Fidelity Check
  -> VERIFIED PROSA SCRIPT
```

## Design invariants

1. **No problem transformation.** The source task model, scheduler, analysis, assumptions, quantifiers, and theorem must be preserved.
2. **Evidence grounding.** ModelIR/AnalysisIR/ProofIR candidates require verbatim source evidence; evidence is located deterministically in the Markdown.
3. **Fail closed.** Ambiguous or missing source semantics are not guessed.
4. **Backend-specific legality.** Unsupported but understood semantics become `NO_MATCH` and an explicit extension contract; unclear source semantics become `INSUFFICIENT_SOURCE`.
5. **Compilation is not enough.** A final semantic-fidelity audit is required.
6. **No trusted proof holes.** Final output is rejected if it contains `Admitted`, `admit`, or `Axiom`.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

A 32B model in 4-bit quantization is the default configuration. Adapt it to the model available on your 48-GB GPU.

## Prosa material

The semantic matcher needs a local Prosa documentation/source tree. Set:

```yaml
prosa:
  docs_dir: /path/to/prosa/docs-or-source
```

The index accepts `.html`, `.md`, `.txt`, and `.v` files.

For best matching, use both generated documentation and the Prosa source tree by pointing `docs_dir` to a directory containing the materials you want indexed.

## Rocq command

Set the command and working directory that compile a `.v` file in your Prosa checkout:

```yaml
rocq:
  command: "rocq compile {file}"
  cwd: /path/to/prosa/worktree
```

If your environment uses `coqc`, change the command, for example:

```yaml
command: "coqc -Q . prosa {file}"
```

The prototype deliberately does not guess your local load paths.

## Run

```bash
cp configs/example.yaml myconfig.yaml
# edit paths
rts2prosa paper.md --config myconfig.yaml
```

Artifacts are emitted in order:

```text
01_chunks.json
02_theory_graph.json
03_model_ir.json
04_analysis_ir.json
05_proof_ir.json
06_semantic_requirements.json
07_prosa_matches.json
08_prosa_ir.json
09_skeleton.v
10_candidate.v
11_rocq_verification.json
12_fidelity.json
FINAL_STATUS.json
VERIFIED_PROSA.v     # only if all gates pass
```

## What is deterministic vs LLM-based?

### Deterministic
- Markdown section/chunk preservation
- evidence quote lookup and line recovery
- Pydantic schema validation
- IR IDs and provenance
- Prosa TF-IDF retrieval
- Rocq process execution
- proof-placeholder audit
- artifact gating

### LLM-based, but constrained and verified
- semantic extraction into ModelIR/AnalysisIR/ProofIR
- claim-entailment verification
- Prosa semantic match classification
- extension contract drafting
- ProsaIR theorem planning
- skeleton/proof completion
- semantic-fidelity audit

For a publication-quality evaluation, use a different model family for semantic verification than for extraction to reduce correlated errors.

## Important limitation

This is an end-to-end research prototype, not a guarantee that arbitrary RTS papers can be formalized automatically. Its important behavior is that it distinguishes:

- supported and faithfully matchable source semantics,
- faithfully compositional matches,
- understood but unsupported semantics requiring a Prosa extension,
- insufficiently specified source semantics.

It only creates `VERIFIED_PROSA.v` after Rocq compilation and the semantic-fidelity gate pass.
