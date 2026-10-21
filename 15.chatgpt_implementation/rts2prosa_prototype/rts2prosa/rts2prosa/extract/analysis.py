from __future__ import annotations

import json
from rts2prosa.common.text import stable_id, normalize_key
from rts2prosa.document.parser import MarkdownChunk
from rts2prosa.ir.base import VerificationSummary
from rts2prosa.ir.model import ModelIR
from rts2prosa.ir.analysis import *
from rts2prosa.llm.structured import StructuredGenerator
from rts2prosa.verify.evidence import verify_quote

SYSTEM = """Extract ANALYSIS SEMANTICS from the current RTS paper, using the verified ModelIR as context. Extract how the model is analyzed: request/demand/supply bounds, curves, workload, interference, busy intervals, response time, search spaces, schedulability conditions, probability bounds, and analysis-specific assumptions. Preserve formulas; do not derive, simplify, or transform them. Do not duplicate system-model facts. A theorem's proof belongs to ProofIR, but a mathematical condition tested by an analysis belongs here. Every item requires an exact evidence quote. Use core AST operations only when faithful; use paper namespace for paper-defined operators; leave AST null if uncertain. Return JSON only."""


def compact_model(m: ModelIR) -> str:
    lines = ["ENTITIES:"] + [f"- {x.name}: {x.kind}" for x in m.entities]
    lines += ["FACTS:"] + [f"- {x.subject} --{x.predicate}--> {x.object}" for x in m.facts]
    lines += ["ASSUMPTIONS:"] + [f"- {x.statement}" for x in m.assumptions]
    lines += ["CONSTRAINTS:"] + [f"- {x.statement}" for x in m.constraints]
    return "\n".join(lines)


class AnalysisExtractor:
    def __init__(self, llm, verifier=None):
        self.gen = StructuredGenerator(llm); self.verifier = verifier

    def extract(self, chunks: list[MarkdownChunk], model: ModelIR) -> AnalysisIR:
        defs, rels, crits, asms, unresolved = [], [], [], [], []
        summary = VerificationSummary(); mctx = compact_model(model)
        for ch in chunks:
            if ch.section.strip().lower() == "references": continue
            prompt = f"VERIFIED MODELIR:\n{mctx}\n\nSECTION:{ch.section}\nSOURCE:\n{ch.text}\n\nSCHEMA:\n{json.dumps(ChunkAnalysisExtraction.model_json_schema(), indent=2)}\nReturn JSON only."
            ex = self.gen.generate(ChunkAnalysisExtraction, SYSTEM, prompt)
            unresolved.extend(ex.unresolved)
            if not ex.analysis_relevant: continue
            for kind, candidates in [("definition",ex.definitions),("relation",ex.relations),("criterion",ex.criteria),("assumption",ex.assumptions)]:
                for c in candidates:
                    summary.extracted += 1
                    ev = verify_quote(ch, c.evidence_quote)
                    if ev is None: summary.rejected += 1; continue
                    summary.evidence_verified += 1
                    if self.verifier:
                        v = self.verifier.verify(c, ev.quote)
                        if v.verdict != "entailed": summary.rejected += 1; continue
                        summary.semantic_verified += 1
                    if kind == "definition":
                        defs.append(AnalysisDefinition(id=stable_id("adef",c.analysis_scope,c.name,c.raw_math or ""), name=c.name, category=c.category, analysis_scope=c.analysis_scope, parameters=c.parameters, description=c.description, raw_math=c.raw_math, expression=c.expression, model_references=c.model_references, evidence=[ev]))
                    elif kind == "relation":
                        rels.append(AnalysisRelation(id=stable_id("arel",c.analysis_scope,c.name,c.raw_math or ""), name=c.name, category=c.category, analysis_scope=c.analysis_scope, description=c.description, variables=c.variables, raw_math=c.raw_math, formula=c.formula, evidence=[ev]))
                    elif kind == "criterion":
                        crits.append(AnalysisCriterion(id=stable_id("acrit",c.analysis_scope,c.name,c.raw_math or ""), name=c.name, analysis_scope=c.analysis_scope, description=c.description, variables=c.variables, raw_math=c.raw_math, condition=c.condition, evidence=[ev]))
                    else:
                        asms.append(AnalysisAssumption(id=stable_id("aasm",c.analysis_scope,c.statement), statement=c.statement, analysis_scope=c.analysis_scope, evidence=[ev]))
        def dedup(items, key):
            d={}
            for x in items:
                k=key(x)
                if k in d:d[k].evidence.extend(x.evidence)
                else:d[k]=x
            return list(d.values())
        defs=dedup(defs,lambda x:(normalize_key(x.analysis_scope),normalize_key(x.name),normalize_key(x.raw_math or "")))
        rels=dedup(rels,lambda x:(normalize_key(x.analysis_scope),normalize_key(x.name),normalize_key(x.raw_math or "")))
        crits=dedup(crits,lambda x:(normalize_key(x.analysis_scope),normalize_key(x.name),normalize_key(x.raw_math or "")))
        asms=dedup(asms,lambda x:(normalize_key(x.analysis_scope),normalize_key(x.statement)))
        return AnalysisIR(paper_id=model.paper_id, model_ir_schema_version=model.schema_version, definitions=defs, relations=rels, criteria=crits, assumptions=asms, unresolved=unresolved, verification=summary)
