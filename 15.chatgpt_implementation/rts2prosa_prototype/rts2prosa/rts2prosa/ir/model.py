from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from rts2prosa.ir.base import EvidenceSpan, Scope, VerificationSummary, UnresolvedItem


class ModelFacet(str, Enum):
    SYSTEM = "system"
    TASK = "task_model"
    JOB = "job_model"
    EXECUTION = "execution_model"
    ARRIVAL = "arrival_model"
    DEADLINE = "deadline_model"
    PROCESSOR = "processor_model"
    RESOURCE = "resource_model"
    SCHEDULER = "scheduler_model"
    PRIORITY = "priority_model"
    PREEMPTION = "preemption_model"
    CRITICALITY = "criticality_model"
    DEPENDENCY = "dependency_model"
    OTHER = "other"


class EntityCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    kind: str
    description: Optional[str] = None
    scope: Scope
    evidence_quote: str


class FactCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    subject: str
    predicate: str
    object: str
    facet: ModelFacet
    scope: Scope
    evidence_quote: str


class AssumptionCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    statement: str
    facet: ModelFacet
    scope: Scope
    evidence_quote: str


class ConstraintCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    statement: str
    raw_math: Optional[str] = None
    facet: ModelFacet
    scope: Scope
    evidence_quote: str


class ChunkModelExtraction(BaseModel):
    model_relevant: bool
    entities: list[EntityCandidate] = Field(default_factory=list)
    facts: list[FactCandidate] = Field(default_factory=list)
    assumptions: list[AssumptionCandidate] = Field(default_factory=list)
    constraints: list[ConstraintCandidate] = Field(default_factory=list)
    unresolved: list[UnresolvedItem] = Field(default_factory=list)


class ModelEntity(BaseModel):
    id: str
    name: str
    kind: str
    description: Optional[str] = None
    evidence: list[EvidenceSpan]


class ModelFact(BaseModel):
    id: str
    subject: str
    predicate: str
    object: str
    facet: ModelFacet
    evidence: list[EvidenceSpan]


class ModelAssumption(BaseModel):
    id: str
    statement: str
    facet: ModelFacet
    evidence: list[EvidenceSpan]


class ModelConstraint(BaseModel):
    id: str
    statement: str
    raw_math: Optional[str] = None
    facet: ModelFacet
    evidence: list[EvidenceSpan]


class SymbolEntry(BaseModel):
    canonical: str
    aliases: list[str] = Field(default_factory=list)
    kind: Optional[str] = None
    source_ids: list[str] = Field(default_factory=list)


class ModelIR(BaseModel):
    schema_version: str = "0.1"
    paper_id: str
    entities: list[ModelEntity] = Field(default_factory=list)
    facts: list[ModelFact] = Field(default_factory=list)
    assumptions: list[ModelAssumption] = Field(default_factory=list)
    constraints: list[ModelConstraint] = Field(default_factory=list)
    symbol_table: list[SymbolEntry] = Field(default_factory=list)
    unresolved: list[UnresolvedItem] = Field(default_factory=list)
    facet_coverage: dict[str, str] = Field(default_factory=dict)
    verification: VerificationSummary = Field(default_factory=VerificationSummary)
