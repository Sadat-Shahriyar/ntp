from __future__ import annotations

from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    model_id: str = "Qwen/Qwen3-32B"
    load_in_4bit: bool = True
    max_new_tokens: int = 3000
    trust_remote_code: bool = False


class ProsaConfig(BaseModel):
    docs_dir: Path
    source_dir: Optional[Path] = None
    top_k: int = 8
    chunk_chars: int = 5000


class RocqConfig(BaseModel):
    command: str = "rocq compile {file}"
    cwd: Optional[Path] = None
    timeout_seconds: int = 120
    max_repair_rounds: int = 6


class PipelineConfig(BaseModel):
    output_dir: Path = Path("outputs")
    markdown_chunk_chars: int = 6000
    semantic_verify: bool = True
    require_fidelity_pass: bool = True
    reject_placeholders: bool = True
    model_llm: LLMConfig = Field(default_factory=LLMConfig)
    verifier_llm: Optional[LLMConfig] = None
    prosa: ProsaConfig
    rocq: RocqConfig = Field(default_factory=RocqConfig)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "PipelineConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data)
