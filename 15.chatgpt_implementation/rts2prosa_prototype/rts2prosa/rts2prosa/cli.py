from __future__ import annotations

import argparse, json

from rts2prosa.config import PipelineConfig
from rts2prosa.llm.hf import HFChatModel
from rts2prosa.pipeline import EndToEndPipeline


def main():
    p=argparse.ArgumentParser(description="RTS paper/Markdown -> verified Prosa/Rocq pipeline")
    p.add_argument("markdown")
    p.add_argument("--config",required=True)
    args=p.parse_args()
    cfg=PipelineConfig.from_yaml(args.config)
    llm=HFChatModel(cfg.model_llm)
    vllm=llm if cfg.verifier_llm is None or cfg.verifier_llm==cfg.model_llm else HFChatModel(cfg.verifier_llm)
    status=EndToEndPipeline(cfg,llm,vllm).run(args.markdown)
    print(json.dumps(status,indent=2))


if __name__=="__main__":main()
