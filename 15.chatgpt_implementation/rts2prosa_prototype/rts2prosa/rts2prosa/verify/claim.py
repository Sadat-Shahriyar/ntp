from __future__ import annotations

import json
from typing import Literal
from pydantic import BaseModel

from rts2prosa.llm.structured import StructuredGenerator


class ClaimVerdict(BaseModel):
    verdict: Literal["entailed", "not_supported", "contradicted", "ambiguous"]
    explanation: str


SYSTEM = """You are a conservative evidence verifier. Decide whether the complete structured claim is directly supported by the quoted source. Use no outside knowledge. Similar terminology is not enough. Return entailed only if all semantic content follows. If opposite, contradicted; if unclear, ambiguous."""


class ClaimVerifier:
    def __init__(self, llm):
        self.gen = StructuredGenerator(llm)

    def verify(self, candidate, quote: str) -> ClaimVerdict:
        prompt = f"""CLAIM:\n{candidate.model_dump_json(indent=2)}\n\nSOURCE QUOTE:\n{quote}\n\nSCHEMA:\n{json.dumps(ClaimVerdict.model_json_schema(), indent=2)}\nReturn JSON only."""
        return self.gen.generate(ClaimVerdict, SYSTEM, prompt, max_new_tokens=400)
