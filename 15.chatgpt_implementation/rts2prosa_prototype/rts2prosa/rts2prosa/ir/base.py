from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class EvidenceSpan(BaseModel):
    chunk_id: str
    section: str
    line_start: int
    line_end: int
    quote: str


class Scope(str, Enum):
    PAPER = "paper"
    BACKGROUND = "background_or_related_work"
    UNCERTAIN = "uncertain"


class VerificationSummary(BaseModel):
    extracted: int = 0
    evidence_verified: int = 0
    semantic_verified: int = 0
    rejected: int = 0
    issues: list[str] = Field(default_factory=list)


class UnresolvedItem(BaseModel):
    topic: str
    reason: str
    source_chunk: Optional[str] = None
    evidence_quote: Optional[str] = None
