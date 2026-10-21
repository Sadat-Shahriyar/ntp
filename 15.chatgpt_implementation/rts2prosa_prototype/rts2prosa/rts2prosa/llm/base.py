from __future__ import annotations

from typing import Protocol


class ChatModel(Protocol):
    def generate(self, system_prompt: str, user_prompt: str, max_new_tokens: int | None = None) -> str:
        ...
