from __future__ import annotations

import json
from pydantic import BaseModel, Field

from rts2prosa.common.text import stable_id
from rts2prosa.ir.model import ModelIR
from rts2prosa.ir.analysis import AnalysisIR
from rts2prosa.ir.proof import ProofIR
from rts2prosa.ir.prosa import *
from rts2prosa.llm.structured import StructuredGenerator
from rts2prosa.prosa.index import ProsaIndex


class MatcherVerdict(BaseModel):
    status: MatchStatus
    rationale: str
    prosa_objects: list[str] = Field(default_factory=list)
    missing_semantics: list[str] = Field(default_factory=list)


SYSTEM = """You are a conservative Prosa semantic matcher. Decide whether the SOURCE semantic requirement can be represented by the retrieved Prosa material WITHOUT changing the source model, analysis, assumptions, quantifiers, or theorem meaning. EXACT_MATCH: one direct semantic counterpart. COMPOSITIONAL_MATCH: exact meaning can be represented by a composition of existing Prosa concepts. NO_MATCH: source semantics are understood but retrieved/existing Prosa does not support them faithfully. INSUFFICIENT_SOURCE: source semantics themselves are underspecified/ambiguous, so faithful matching cannot be decided. Never use a merely similar deterministic abstraction for a probabilistic source concept if probability semantics are lost. Return JSON only."""


def requirements_from_ir(model:ModelIR,analysis:AnalysisIR,proof:ProofIR)->list[SemanticRequirement]:
    req=[]
    def add(layer,kind,name,sem,evidence):
        req.append(SemanticRequirement(id=stable_id("req",layer,kind,name,sem),layer=layer,source_kind=kind,source_name=name,semantics=sem,evidence=evidence))
    for x in model.facts:add("ModelIR","fact",f"{x.subject}:{x.predicate}",x.object,[e.quote for e in x.evidence])
    for x in model.assumptions:add("ModelIR","assumption",x.id,x.statement,[e.quote for e in x.evidence])
    for x in model.constraints:add("ModelIR","constraint",x.id,x.raw_math or x.statement,[e.quote for e in x.evidence])
    for x in analysis.definitions:add("AnalysisIR",x.category.value,x.name,x.raw_math or x.description,[e.quote for e in x.evidence])
    for x in analysis.relations:add("AnalysisIR",x.category.value,x.name,x.raw_math or x.description,[e.quote for e in x.evidence])
    for x in analysis.criteria:add("AnalysisIR","criterion",x.name,x.raw_math or x.description,[e.quote for e in x.evidence])
    for x in proof.theorems:add("ProofIR","theorem",x.name,x.statement_text,[e.quote for e in x.evidence])
    return req


class ProsaMatcher:
    def __init__(self,llm,index:ProsaIndex,top_k:int=8):
        self.gen=StructuredGenerator(llm);self.index=index;self.top_k=top_k

    def match(self, requirements:list[SemanticRequirement])->list[MatchDecision]:
        out=[]
        for r in requirements:
            hits=self.index.search(r.semantics+" "+r.source_name,top_k=self.top_k)
            snippets=[]; pe=[]
            for d,s in hits:
                snippets.append(f"DOC {d.doc_id} TITLE={d.title} PATH={d.path} SCORE={s:.4f}\n{d.text[:5000]}")
                pe.append(ProsaEvidence(doc_id=d.doc_id,title=d.title,path=d.path,snippet=d.text[:1200],score=s))
            prompt=f"SOURCE REQUIREMENT:\n{r.model_dump_json(indent=2)}\n\nRETRIEVED PROSA MATERIAL:\n{'\n\n'.join(snippets) if snippets else '[NONE]'}\n\nSCHEMA:\n{json.dumps(MatcherVerdict.model_json_schema(),indent=2)}\nReturn JSON only."
            v=self.gen.generate(MatcherVerdict,SYSTEM,prompt,max_new_tokens=1000)
            out.append(MatchDecision(requirement_id=r.id,status=v.status,rationale=v.rationale,prosa_objects=v.prosa_objects,prosa_evidence=pe,missing_semantics=v.missing_semantics))
        return out
