from __future__ import annotations

import json
from pydantic import BaseModel, Field

from rts2prosa.common.text import stable_id
from rts2prosa.ir.proof import ProofIR
from rts2prosa.ir.prosa import *
from rts2prosa.llm.structured import StructuredGenerator


class ExtensionDraft(BaseModel):
    name: str
    semantic_contract: str
    proposed_definitions: list[str] = Field(default_factory=list)
    proof_obligations: list[str] = Field(default_factory=list)


class TheoremPlanDraft(BaseModel):
    target_name: str
    imports: list[str] = Field(default_factory=list)
    contexts: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    candidate_lemmas: list[str] = Field(default_factory=list)
    theorem_templates: list[str] = Field(default_factory=list)
    extension_ids: list[str] = Field(default_factory=list)


SYSTEM_EXT="""Design a minimal Prosa/Rocq extension contract for SOURCE semantics that have NO_MATCH. Preserve the original source semantics exactly. Do not reduce to a different problem. The output is a specification, not an assertion that the extension is already verified. State definitions and proof obligations needed before the extension may be trusted."""
SYSTEM_PLAN="""Construct a Prosa target plan for the source theorem using ONLY matched Prosa objects/evidence plus explicitly listed extension specs. Do not invent library identifiers. If an exact identifier is unavailable, omit it rather than guessing. Preserve source theorem semantics."""


class Legalizer:
    def __init__(self,llm):self.gen=StructuredGenerator(llm)

    def build(self,paper_id:str,requirements:list[SemanticRequirement],matches:list[MatchDecision],proof:ProofIR)->ProsaIR:
        req_by={r.id:r for r in requirements}; extensions=[]
        for m in matches:
            if m.status==MatchStatus.NO_MATCH:
                r=req_by[m.requirement_id]
                prompt=f"SOURCE REQUIREMENT:\n{r.model_dump_json(indent=2)}\nMISSING SEMANTICS:\n{json.dumps(m.missing_semantics)}\nSCHEMA:\n{json.dumps(ExtensionDraft.model_json_schema(),indent=2)}"
                d=self.gen.generate(ExtensionDraft,SYSTEM_EXT,prompt,max_new_tokens=1200)
                extensions.append(ExtensionSpec(id=stable_id("ext",r.id,d.name),name=d.name,source_requirement_ids=[r.id],semantic_contract=d.semantic_contract,proposed_definitions=d.proposed_definitions,proof_obligations=d.proof_obligations,verified=False))
        symbols=[ProsaSymbol(source_requirement_id=m.requirement_id,prosa_names=m.prosa_objects,status=m.status) for m in matches]
        plans=[]
        match_text="\n".join(f"{m.requirement_id}: {m.status.value}; objects={m.prosa_objects}; rationale={m.rationale}" for m in matches)
        ext_text="\n".join(e.model_dump_json(indent=2) for e in extensions)
        for t in proof.theorems:
            prompt=f"SOURCE THEOREM:\n{t.model_dump_json(indent=2)}\n\nMATCHES:\n{match_text}\n\nEXTENSIONS:\n{ext_text}\n\nSCHEMA:\n{json.dumps(TheoremPlanDraft.model_json_schema(),indent=2)}"
            d=self.gen.generate(TheoremPlanDraft,SYSTEM_PLAN,prompt,max_new_tokens=1800)
            plans.append(ProsaTheoremPlan(source_theorem_id=t.id,target_name=d.target_name,imports=d.imports,contexts=d.contexts,hypotheses=d.hypotheses,candidate_lemmas=d.candidate_lemmas,theorem_templates=d.theorem_templates,extension_ids=d.extension_ids))
        insuff=any(m.status==MatchStatus.INSUFFICIENT_SOURCE for m in matches)
        reqext=bool(extensions)
        exact_existing=not insuff and not reqext and all(m.status in {MatchStatus.EXACT_MATCH,MatchStatus.COMPOSITIONAL_MATCH} for m in matches)
        return ProsaIR(paper_id=paper_id,requirements=requirements,matches=matches,extensions=extensions,symbols=symbols,theorem_plans=plans,formalizable_with_existing_prosa=exact_existing,requires_extension=reqext,insufficient_source=insuff)
