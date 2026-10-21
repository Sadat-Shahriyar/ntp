from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from rts2prosa.common.expressions import ExprNode
from rts2prosa.ir.base import EvidenceSpan, VerificationSummary, UnresolvedItem


class AnalysisCategory(str, Enum):
    REQUEST_BOUND = "request_bound"
    DEMAND_BOUND = "demand_bound"
    SUPPLY_BOUND = "supply_bound"
    REQUEST_CURVE = "request_curve"
    SERVICE_CURVE = "service_curve"
    WORKLOAD = "workload"
    INTERFERENCE = "interference"
    BUSY_INTERVAL = "busy_interval"
    RESPONSE_TIME = "response_time"
    SEARCH_SPACE = "search_space"
    SCHEDULABILITY = "schedulability"
    PROBABILITY_BOUND = "probability_bound"
    CURVE_RELATION = "curve_relation"
    OTHER = "other"


class VariableDecl(BaseModel):
    name: str
    semantic_type: Optional[str] = None
    domain_description: Optional[str] = None


class AnalysisDefinitionCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    category: AnalysisCategory
    analysis_scope: str
    parameters: list[VariableDecl] = Field(default_factory=list)
    description: str
    raw_math: Optional[str] = None
    expression: Optional[ExprNode] = None
    model_references: list[str] = Field(default_factory=list)
    evidence_quote: str


class AnalysisRelationCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    category: AnalysisCategory
    analysis_scope: str
    description: str
    variables: list[VariableDecl] = Field(default_factory=list)
    raw_math: Optional[str] = None
    formula: Optional[ExprNode] = None
    evidence_quote: str


class AnalysisCriterionCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    analysis_scope: str
    description: str
    variables: list[VariableDecl] = Field(default_factory=list)
    raw_math: Optional[str] = None
    condition: Optional[ExprNode] = None
    evidence_quote: str


class ChunkAnalysisExtraction(BaseModel):
    analysis_relevant: bool
    definitions: list[AnalysisDefinitionCandidate] = Field(default_factory=list)
    relations: list[AnalysisRelationCandidate] = Field(default_factory=list)
    criteria: list[AnalysisCriterionCandidate] = Field(default_factory=list)
    assumptions: list[AssumptionCandidate] = Field(default_factory=list)
    unresolved: list[UnresolvedItem] = Field(default_factory=list)


class AssumptionCandidate(BaseModel):
    statement: str
    analysis_scope: str
    evidence_quote: str


class AnalysisDefinition(BaseModel):
    id: str
    name: str
    category: AnalysisCategory
    analysis_scope: str
    parameters: list[VariableDecl]
    description: str
    raw_math: Optional[str] = None
    expression: Optional[ExprNode] = None
    model_references: list[str]
    evidence: list[EvidenceSpan]


class AnalysisRelation(BaseModel):
    id: str
    name: str
    category: AnalysisCategory
    analysis_scope: str
    description: str
    variables: list[VariableDecl]
    raw_math: Optional[str] = None
    formula: Optional[ExprNode] = None
    evidence: list[EvidenceSpan]


class AnalysisCriterion(BaseModel):
    id: str
    name: str
    analysis_scope: str
    description: str
    variables: list[VariableDecl]
    raw_math: Optional[str] = None
    condition: Optional[ExprNode] = None
    evidence: list[EvidenceSpan]


class AnalysisAssumption(BaseModel):
    id: str
    statement: str
    analysis_scope: str
    evidence: list[EvidenceSpan]


class AnalysisIR(BaseModel):
    schema_version: str = "0.1"
    paper_id: str
    model_ir_schema_version: str
    definitions: list[AnalysisDefinition] = Field(default_factory=list)
    relations: list[AnalysisRelation] = Field(default_factory=list)
    criteria: list[AnalysisCriterion] = Field(default_factory=list)
    assumptions: list[AnalysisAssumption] = Field(default_factory=list)
    unresolved: list[UnresolvedItem] = Field(default_factory=list)
    verification: VerificationSummary = Field(default_factory=VerificationSummary)
