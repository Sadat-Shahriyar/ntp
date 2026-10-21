from __future__ import annotations

import json
from rts2prosa.common.text import stable_id, normalize_key
from rts2prosa.document.parser import MarkdownChunk
from rts2prosa.ir.base import VerificationSummary
from rts2prosa.ir.model import ModelIR
from rts2prosa.ir.analysis import AnalysisIR
from rts2prosa.ir.proof import *
from rts2prosa.llm.structured import StructuredGenerator
from rts2prosa.verify.evidence import verify_quote

SYSTEM = """Extract theorem semantics and proof structure from the CURRENT PAPER. Preserve the theorem exactly: quantified variables, hypotheses, conclusion, cited dependencies, references to verified ModelIR and AnalysisIR objects, and the paper's proof sketch. Do not strengthen/weaken the theorem, invent assumptions, or replace it by a known theorem. Decompose the proof sketch into explicit proof obligations only when they are logically required by the stated theorem/proof and clearly justified by source context; otherwise mark uncertainty. Every theorem requires verbatim evidence. Return JSON only."""


def compact_ir(model: ModelIR, analysis: AnalysisIR) -> str:
    return "MODEL IDS:\n" + "\n".join(f"- {x.id}: {getattr(x,'name',getattr(x,'statement',''))}" for x in model.entities+model.facts+model.assumptions+model.constraints) + "\nANALYSIS IDS:\n" + "\n".join(f"- {x.id}: {getattr(x,'name',getattr(x,'statement',''))}" for x in analysis.definitions+analysis.relations+analysis.criteria+analysis.assumptions)


class ObligationBatch(BaseModel):
    obligations: list[ProofObligation] = Field(default_factory=list)


class ProofExtractor:
    def __init__(self, llm, verifier=None):
        self.gen=StructuredGenerator(llm); self.verifier=verifier

    def extract(self, chunks:list[MarkdownChunk], model:ModelIR, analysis:AnalysisIR)->ProofIR:
        thms=[]; unresolved=[]; summary=VerificationSummary(); ctx=compact_ir(model,analysis)
        for ch in chunks:
            if ch.section.strip().lower()=="references":continue
            prompt=f"VERIFIED IR OBJECTS:\n{ctx}\n\nSECTION:{ch.section}\nSOURCE:\n{ch.text}\n\nSCHEMA:\n{json.dumps(ChunkProofExtraction.model_json_schema(),indent=2)}\nReturn JSON only."
            ex=self.gen.generate(ChunkProofExtraction,SYSTEM,prompt)
            unresolved.extend(ex.unresolved)
            if not ex.proof_relevant:continue
            for c in ex.theorems:
                summary.extracted+=1; ev=verify_quote(ch,c.evidence_quote)
                if ev is None: summary.rejected+=1; continue
                summary.evidence_verified+=1
                if self.verifier:
                    v=self.verifier.verify(c,ev.quote)
                    if v.verdict!="entailed":summary.rejected+=1;continue
                    summary.semantic_verified+=1
                tid=stable_id("thm",c.name,c.statement_text)
                deps=[]
                for rid in c.model_references+c.analysis_references:
                    deps.append(ProofDependency(source_id=rid, relation="requires"))
                # Obligation synthesis is a separate constrained call using the accepted theorem.
                op_prompt=f"""THEOREM:\n{c.model_dump_json(indent=2)}\n\nCreate conservative proof obligations needed to mechanize this theorem, based only on this theorem and proof sketch. Do not invent domain assumptions. If a step is missing in the source, describe it as an obligation rather than assuming it. IDs must be unique strings.\nSCHEMA:\n{json.dumps(ObligationBatch.model_json_schema(),indent=2)}\nReturn JSON only."""
                ob=self.gen.generate(ObligationBatch,SYSTEM,op_prompt,max_new_tokens=1600)
                thms.append(FormalTheorem(id=tid,name=c.name,theorem_scope=c.theorem_scope,statement_text=c.statement_text,quantified_variables=c.quantified_variables,hypotheses=c.hypotheses,conclusion_text=c.conclusion_text,conclusion=c.conclusion,model_references=c.model_references,analysis_references=c.analysis_references,dependencies=deps,obligations=ob.obligations,proof_sketch=c.proof_sketch,evidence=[ev]))
        # merge exact repeats
        d={}
        for t in thms:
            k=(normalize_key(t.name),normalize_key(t.statement_text))
            if k in d:d[k].evidence.extend(t.evidence)
            else:d[k]=t
        return ProofIR(paper_id=model.paper_id,model_ir_schema_version=model.schema_version,analysis_ir_schema_version=analysis.schema_version,theorems=list(d.values()),unresolved=unresolved,verification=summary)
