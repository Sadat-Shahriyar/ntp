from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MatchStatus(str, Enum):
    EXACT_MATCH = "EXACT_MATCH"
    COMPOSITIONAL_MATCH = "COMPOSITIONAL_MATCH"
    NO_MATCH = "NO_MATCH"
    INSUFFICIENT_SOURCE = "INSUFFICIENT_SOURCE"


class ProsaEvidence(BaseModel):
    doc_id: str
    title: str
    path: str
    snippet: str
    score: float


class SemanticRequirement(BaseModel):
    id: str
    layer: str
    source_kind: str
    source_name: str
    semantics: str
    evidence: list[str] = Field(default_factory=list)


class MatchDecision(BaseModel):
    requirement_id: str
    status: MatchStatus
    rationale: str
    prosa_objects: list[str] = Field(default_factory=list)
    prosa_evidence: list[ProsaEvidence] = Field(default_factory=list)
    missing_semantics: list[str] = Field(default_factory=list)


class ExtensionSpec(BaseModel):
    id: str
    name: str
    source_requirement_ids: list[str]
    semantic_contract: str
    proposed_definitions: list[str] = Field(default_factory=list)
    proof_obligations: list[str] = Field(default_factory=list)
    verified: bool = False


class ProsaSymbol(BaseModel):
    source_requirement_id: str
    prosa_names: list[str]
    status: MatchStatus


class ProsaTheoremPlan(BaseModel):
    source_theorem_id: str
    target_name: str
    imports: list[str] = Field(default_factory=list)
    contexts: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    candidate_lemmas: list[str] = Field(default_factory=list)
    theorem_templates: list[str] = Field(default_factory=list)
    extension_ids: list[str] = Field(default_factory=list)


class ProsaIR(BaseModel):
    schema_version: str = "0.1"
    paper_id: str
    requirements: list[SemanticRequirement]
    matches: list[MatchDecision]
    extensions: list[ExtensionSpec] = Field(default_factory=list)
    symbols: list[ProsaSymbol] = Field(default_factory=list)
    theorem_plans: list[ProsaTheoremPlan] = Field(default_factory=list)
    formalizable_with_existing_prosa: bool
    requires_extension: bool
    insufficient_source: bool
