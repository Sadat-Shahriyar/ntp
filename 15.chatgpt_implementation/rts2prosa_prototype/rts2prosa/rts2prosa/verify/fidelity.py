from __future__ import annotations

import json, re
from typing import Literal
from pydantic import BaseModel, Field

from rts2prosa.ir.model import ModelIR
from rts2prosa.ir.analysis import AnalysisIR
from rts2prosa.ir.proof import ProofIR
from rts2prosa.ir.prosa import ProsaIR
from rts2prosa.llm.structured import StructuredGenerator


class FidelityCheck(BaseModel):
    status: Literal["pass","fail","uncertain"]
    preserved_model: bool
    preserved_analysis: bool
    preserved_theorem: bool
    dropped_assumptions: list[str] = Field(default_factory=list)
    added_assumptions: list[str] = Field(default_factory=list)
    changed_quantifiers: list[str] = Field(default_factory=list)
    changed_conclusions: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


SYSTEM="""Perform a semantic-fidelity audit between the source IRs and final Rocq/Prosa script. The core invariant is that the source problem is NOT transformed: preserve system model, analysis definitions/conditions, assumptions, quantifiers, and theorem conclusion. Compilation does not imply semantic fidelity. Fail if the script drops or adds material assumptions, changes scheduler/processor/preemption/task semantics, replaces probabilistic concepts by deterministic ones, weakens/strengthens the theorem, or otherwise formalizes a different result. Be conservative. Return JSON only."""


class FidelityVerifier:
    def __init__(self,llm):self.gen=StructuredGenerator(llm)

    def verify(self,model:ModelIR,analysis:AnalysisIR,proof:ProofIR,prosa:ProsaIR,script:str)->FidelityCheck:
        prompt=f"MODELIR:\n{model.model_dump_json(indent=2)}\n\nANALYSISIR:\n{analysis.model_dump_json(indent=2)}\n\nPROOFIR:\n{proof.model_dump_json(indent=2)}\n\nPROSAIR:\n{prosa.model_dump_json(indent=2)}\n\nFINAL SCRIPT:\n{script}\n\nSCHEMA:\n{json.dumps(FidelityCheck.model_json_schema(),indent=2)}"
        out=self.gen.generate(FidelityCheck,SYSTEM,prompt,max_new_tokens=1800)
        # deterministic trust audit overrides any optimistic model verdict
        if re.search(r"\b(Admitted|admit|Axiom)\b",script):
            out.status="fail";out.notes.append("deterministic trust audit found proof placeholder/axiom")
        if not (out.preserved_model and out.preserved_analysis and out.preserved_theorem):out.status="fail"
        return out
