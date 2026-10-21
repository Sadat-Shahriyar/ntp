from __future__ import annotations

import json
from typing import TypeVar, Type
from pydantic import BaseModel, ValidationError

from rts2prosa.common.text import strip_code_fences

T = TypeVar("T", bound=BaseModel)


def extract_json(text: str) -> dict:
    text = strip_code_fences(text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start < 0 or end < start:
            raise
        return json.loads(text[start:end + 1])


class StructuredGenerator:
    def __init__(self, llm, max_retries: int = 2):
        self.llm = llm
        self.max_retries = max_retries

    def generate(self, schema: Type[T], system_prompt: str, user_prompt: str, max_new_tokens: int | None = None) -> T:
        current_prompt = user_prompt
        last_error = None
        for _ in range(self.max_retries + 1):
            raw = self.llm.generate(system_prompt, current_prompt, max_new_tokens=max_new_tokens)
            try:
                return schema.model_validate(extract_json(raw))
            except (ValidationError, json.JSONDecodeError) as e:
                last_error = e
                current_prompt = (
                    user_prompt
                    + "\n\nYour previous output was invalid. Return JSON only and obey the schema exactly. "
                    + f"Validation error: {e}"
                )
        raise RuntimeError(f"structured generation failed: {last_error}")
