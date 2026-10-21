from __future__ import annotations

import re
from pathlib import Path
from pydantic import BaseModel

from rts2prosa.prosa.index import ProsaIndex
from rts2prosa.rocq.compiler import RocqCompiler, CompileResult

HOLE_RE=re.compile(r"\(\*\s*HOLE:([^*]+?)\s*\*\)\s*Admitted\.")
PLACEHOLDER_RE=re.compile(r"\b(Admitted|admit|Axiom)\b")


class CompletionResult(BaseModel):
    success: bool
    rounds: int
    script: str
    compile_result: CompileResult
    remaining_holes: list[str]


SYSTEM_HOLE="""Fill exactly one Rocq proof hole in a Prosa development. Return ONLY the proof replacement text including Proof. ... Qed. Use the local context and retrieved Prosa material. Do not change the theorem statement, assumptions, model, or analysis. Do not use Admitted, admit, Axiom, or invented identifiers."""
SYSTEM_REPAIR="""Repair this Rocq/Prosa script using the compiler error. Preserve all source theorem semantics and statements; only correct target-level proof/code issues. Do not add assumptions, weaken conclusions, switch models, use Admitted/admit/Axiom, or invent Prosa identifiers. Return the full corrected Rocq script only."""


class ProofCompleter:
    def __init__(self,llm,index:ProsaIndex,compiler:RocqCompiler,max_rounds:int=6):
        self.llm=llm;self.index=index;self.compiler=compiler;self.max_rounds=max_rounds

    def _fill_holes(self,script:str)->str:
        while True:
            m=HOLE_RE.search(script)
            if not m:break
            hid=m.group(1).strip()
            context=script[max(0,m.start()-7000):m.start()]
            hits=self.index.search(context[-3000:],top_k=6)
            docs="\n\n".join(d.text[:3500] for d,_ in hits)
            prompt=f"HOLE ID:{hid}\n\nSCRIPT CONTEXT:\n{context}\n\nRETRIEVED PROSA:\n{docs}"
            proof=self.llm.generate(SYSTEM_HOLE,prompt,max_new_tokens=2200).strip()
            script=script[:m.start()]+proof+script[m.end():]
        return script

    def run(self,script:str,path:str|Path)->CompletionResult:
        path=Path(path); rounds=0
        script=self._fill_holes(script)
        path.write_text(script,encoding="utf-8")
        res=self.compiler.compile(path)
        while not res.success and rounds<self.max_rounds:
            rounds+=1
            hits=self.index.search((res.stderr or res.stdout)[-4000:],top_k=6)
            docs="\n\n".join(d.text[:2500] for d,_ in hits)
            prompt=f"COMPILER COMMAND:{res.command}\nERROR:\n{res.stderr}\n{res.stdout}\n\nPROSA MATERIAL:\n{docs}\n\nSCRIPT:\n{script}"
            repaired=self.llm.generate(SYSTEM_REPAIR,prompt,max_new_tokens=9000).strip()
            script=repaired; path.write_text(script,encoding="utf-8");res=self.compiler.compile(path)
        holes=[x.strip() for x in HOLE_RE.findall(script)]
        safe=not PLACEHOLDER_RE.search(script)
        return CompletionResult(success=res.success and not holes and safe,rounds=rounds,script=script,compile_result=res,remaining_holes=holes)
