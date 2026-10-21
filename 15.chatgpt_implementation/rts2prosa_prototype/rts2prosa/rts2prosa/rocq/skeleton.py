from __future__ import annotations

from pydantic import BaseModel

from rts2prosa.ir.proof import ProofIR
from rts2prosa.ir.prosa import ProsaIR


class ScriptDraft(BaseModel):
    script: str


SYSTEM="""Generate a Rocq/Prosa source skeleton from the supplied ProsaIR and source ProofIR. Use only exact Prosa identifiers listed in ProsaIR; never invent library names. Preserve theorem semantics. Every unfinished proof must use a uniquely named marker exactly as: (* HOLE:<id> *) Admitted. Do not use Axiom/admit. If ProsaIR reports insufficient_source, do not fabricate a theorem. If extensions are required, include explicit extension sections first with their proof obligations as holes. Return only Rocq code."""


class SkeletonGenerator:
    def __init__(self,llm):self.llm=llm

    def generate(self,proof:ProofIR,prosa:ProsaIR)->str:
        prompt=f"PROOFIR:\n{proof.model_dump_json(indent=2)}\n\nPROSAIR:\n{prosa.model_dump_json(indent=2)}"
        return self.llm.generate(SYSTEM,prompt,max_new_tokens=7000).strip()
