from __future__ import annotations

import json
from collections import defaultdict

from rts2prosa.common.text import stable_id, normalize_key
from rts2prosa.document.parser import MarkdownChunk
from rts2prosa.ir.base import VerificationSummary
from rts2prosa.ir.model import *
from rts2prosa.llm.structured import StructuredGenerator
from rts2prosa.verify.evidence import verify_quote

SYSTEM = """Extract only the CURRENT PAPER'S real-time SYSTEM MODEL. Do not summarize and do not infer conventional RTS assumptions. Extract tasks/jobs, parameters, execution/arrival/deadline/processor/resource/scheduler/priority/preemption models, explicit relations, assumptions, constraints. Do not extract workload/interference/response-time/schedulability-analysis definitions. Do not transform the source problem. Every item requires an exact verbatim evidence_quote. Background/related-work claims must be scoped as background_or_related_work. Ambiguous information goes to unresolved. Return JSON only."""


class ModelExtractor:
    def __init__(self, llm, verifier=None):
        self.gen = StructuredGenerator(llm)
        self.verifier = verifier

    def _prompt(self, ch: MarkdownChunk):
        return f"SECTION: {ch.section}\nPATH: {' > '.join(ch.heading_path)}\nSOURCE:\n{ch.text}\n\nSCHEMA:\n{json.dumps(ChunkModelExtraction.model_json_schema(), indent=2)}\nReturn JSON only."

    def extract(self, paper_id: str, chunks: list[MarkdownChunk]) -> ModelIR:
        entities, facts, assumptions, constraints, unresolved = [], [], [], [], []
        summary = VerificationSummary()
        for ch in chunks:
            if ch.section.strip().lower() == "references":
                continue
            ex = self.gen.generate(ChunkModelExtraction, SYSTEM, self._prompt(ch))
            unresolved.extend(ex.unresolved)
            if not ex.model_relevant:
                continue
            for bucket_name in ["entities", "facts", "assumptions", "constraints"]:
                for c in getattr(ex, bucket_name):
                    if getattr(c, "scope", None) != Scope.PAPER:
                        continue
                    summary.extracted += 1
                    ev = verify_quote(ch, c.evidence_quote)
                    if ev is None:
                        summary.rejected += 1; continue
                    summary.evidence_verified += 1
                    if self.verifier is not None:
                        v = self.verifier.verify(c, ev.quote)
                        if v.verdict != "entailed":
                            summary.rejected += 1; continue
                        summary.semantic_verified += 1
                    if bucket_name == "entities":
                        entities.append(ModelEntity(id=stable_id("ent", c.name, c.kind), name=c.name, kind=c.kind, description=c.description, evidence=[ev]))
                    elif bucket_name == "facts":
                        facts.append(ModelFact(id=stable_id("fact", c.subject, c.predicate, c.object), subject=c.subject, predicate=c.predicate, object=c.object, facet=c.facet, evidence=[ev]))
                    elif bucket_name == "assumptions":
                        assumptions.append(ModelAssumption(id=stable_id("asm", c.statement), statement=c.statement, facet=c.facet, evidence=[ev]))
                    else:
                        constraints.append(ModelConstraint(id=stable_id("con", c.statement, c.raw_math or ""), statement=c.statement, raw_math=c.raw_math, facet=c.facet, evidence=[ev]))
        def dedup(items, keyfn):
            d = {}
            for x in items:
                k = keyfn(x)
                if k in d: d[k].evidence.extend(x.evidence)
                else: d[k] = x
            return list(d.values())
        entities = dedup(entities, lambda x:(normalize_key(x.name), normalize_key(x.kind)))
        facts = dedup(facts, lambda x:(normalize_key(x.subject), normalize_key(x.predicate), normalize_key(x.object)))
        assumptions = dedup(assumptions, lambda x:normalize_key(x.statement))
        constraints = dedup(constraints, lambda x:(normalize_key(x.statement), normalize_key(x.raw_math or "")))
        symbols = [SymbolEntry(canonical=e.name, aliases=[], kind=e.kind, source_ids=[e.id]) for e in entities]
        known = {normalize_key(s.canonical) for s in symbols}
        for f in facts:
            if normalize_key(f.subject) not in known:
                symbols.append(SymbolEntry(canonical=f.subject, aliases=[], kind=None, source_ids=[f.id])); known.add(normalize_key(f.subject))
        coverage = {}
        for facet in ModelFacet:
            hit = any(x.facet == facet for x in facts + assumptions + constraints)
            coverage[facet.value] = "found" if hit else "not_found"
        # potential conflicts, conservatively surfaced
        by = defaultdict(set)
        for f in facts: by[(normalize_key(f.subject), normalize_key(f.predicate))].add(normalize_key(f.object))
        for k, vals in by.items():
            if len(vals) > 1: summary.issues.append(f"potential conflict {k}: {sorted(vals)}")
        return ModelIR(paper_id=paper_id, entities=entities, facts=facts, assumptions=assumptions, constraints=constraints, symbol_table=symbols, unresolved=unresolved, facet_coverage=coverage, verification=summary)
