from __future__ import annotations

from pathlib import Path

from rts2prosa.config import PipelineConfig
from rts2prosa.common.io import ensure_dir,dump_json
from rts2prosa.document.parser import read_and_chunk
from rts2prosa.document.theory import build_theory_graph
from rts2prosa.extract.model import ModelExtractor
from rts2prosa.extract.analysis import AnalysisExtractor
from rts2prosa.extract.proof import ProofExtractor
from rts2prosa.verify.claim import ClaimVerifier
from rts2prosa.verify.fidelity import FidelityVerifier
from rts2prosa.prosa.index import load_prosa_docs,ProsaIndex
from rts2prosa.prosa.matcher import ProsaMatcher,requirements_from_ir
from rts2prosa.prosa.legalize import Legalizer
from rts2prosa.rocq.skeleton import SkeletonGenerator
from rts2prosa.rocq.compiler import RocqCompiler
from rts2prosa.rocq.completion import ProofCompleter


class EndToEndPipeline:
    def __init__(self,cfg:PipelineConfig,extractor_llm,verifier_llm=None):
        self.cfg=cfg;self.llm=extractor_llm;self.vllm=verifier_llm or extractor_llm
        self.claim_verifier=ClaimVerifier(self.vllm) if cfg.semantic_verify else None
        docs=load_prosa_docs(cfg.prosa.docs_dir,cfg.prosa.chunk_chars)
        self.prosa_index=ProsaIndex(docs)

    def run(self,markdown_path:str|Path):
        markdown_path=Path(markdown_path); out=ensure_dir(self.cfg.output_dir / markdown_path.stem)
        _,chunks=read_and_chunk(markdown_path,self.cfg.markdown_chunk_chars)
        dump_json([c.__dict__ for c in chunks],out/"01_chunks.json")
        graph=build_theory_graph(chunks);dump_json(graph,out/"02_theory_graph.json")
        model=ModelExtractor(self.llm,self.claim_verifier).extract(markdown_path.stem,chunks);dump_json(model,out/"03_model_ir.json")
        analysis=AnalysisExtractor(self.llm,self.claim_verifier).extract(chunks,model);dump_json(analysis,out/"04_analysis_ir.json")
        proof=ProofExtractor(self.llm,self.claim_verifier).extract(chunks,model,analysis);dump_json(proof,out/"05_proof_ir.json")
        req=requirements_from_ir(model,analysis,proof);dump_json([x.model_dump(mode="json") for x in req],out/"06_semantic_requirements.json")
        matches=ProsaMatcher(self.vllm,self.prosa_index,self.cfg.prosa.top_k).match(req);dump_json([x.model_dump(mode="json") for x in matches],out/"07_prosa_matches.json")
        prosa=Legalizer(self.llm).build(model.paper_id,req,matches,proof);dump_json(prosa,out/"08_prosa_ir.json")
        if prosa.insufficient_source:
            status={"verified":False,"reason":"INSUFFICIENT_SOURCE","output_dir":str(out)};dump_json(status,out/"FINAL_STATUS.json");return status
        skeleton=SkeletonGenerator(self.llm).generate(proof,prosa);(out/"09_skeleton.v").write_text(skeleton,encoding="utf-8")
        compiler=RocqCompiler(self.cfg.rocq)
        comp=ProofCompleter(self.llm,self.prosa_index,compiler,self.cfg.rocq.max_repair_rounds).run(skeleton,out/"10_candidate.v")
        dump_json(comp,out/"11_rocq_verification.json")
        if not comp.success:
            status={"verified":False,"reason":"ROCQ_VERIFICATION_FAILED","output_dir":str(out)};dump_json(status,out/"FINAL_STATUS.json");return status
        fidelity=FidelityVerifier(self.vllm).verify(model,analysis,proof,prosa,comp.script);dump_json(fidelity,out/"12_fidelity.json")
        verified=fidelity.status=="pass" if self.cfg.require_fidelity_pass else fidelity.status!="fail"
        if verified and prosa.extensions:
            # An extension is considered verified only after the generated extension
            # obligations compile without placeholders AND the source-to-target fidelity
            # audit passes. This is stricter than merely generating an extension spec.
            for ext in prosa.extensions:
                ext.verified=True
            dump_json(prosa,out/"13_prosa_ir_verified.json")
        final=out/"VERIFIED_PROSA.v"
        if verified: final.write_text(comp.script,encoding="utf-8")
        status={"verified":verified,"reason":"OK" if verified else "SEMANTIC_FIDELITY_FAILED","script":str(final) if verified else None,"output_dir":str(out),"extensions_verified":all(e.verified for e in prosa.extensions) if prosa.extensions else True}
        dump_json(status,out/"FINAL_STATUS.json");return status
