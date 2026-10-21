from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field

from rts2prosa.common.expressions import ExprNode
from rts2prosa.ir.base import EvidenceSpan, VerificationSummary, UnresolvedItem
from rts2prosa.ir.analysis import VariableDecl


class ProofDependency(BaseModel):
    source_id: str
    relation: Literal["uses_definition", "uses_lemma", "uses_assumption", "requires"]


class ProofObligation(BaseModel):
    id: str
    description: str
    formula: Optional[ExprNode] = None
    raw_math: Optional[str] = None
    dependency_ids: list[str] = Field(default_factory=list)


class TheoremCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    theorem_scope: str
    statement_text: str
    quantified_variables: list[VariableDecl] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    conclusion_text: str
    conclusion: Optional[ExprNode] = None
    model_references: list[str] = Field(default_factory=list)
    analysis_references: list[str] = Field(default_factory=list)
    cited_dependencies: list[str] = Field(default_factory=list)
    proof_sketch: Optional[str] = None
    evidence_quote: str


class ChunkProofExtraction(BaseModel):
    proof_relevant: bool
    theorems: list[TheoremCandidate] = Field(default_factory=list)
    unresolved: list[UnresolvedItem] = Field(default_factory=list)


class FormalTheorem(BaseModel):
    id: str
    name: str
    theorem_scope: str
    statement_text: str
    quantified_variables: list[VariableDecl]
    hypotheses: list[str]
    conclusion_text: str
    conclusion: Optional[ExprNode] = None
    model_references: list[str]
    analysis_references: list[str]
    dependencies: list[ProofDependency] = Field(default_factory=list)
    obligations: list[ProofObligation] = Field(default_factory=list)
    proof_sketch: Optional[str] = None
    evidence: list[EvidenceSpan]


class ProofIR(BaseModel):
    schema_version: str = "0.1"
    paper_id: str
    model_ir_schema_version: str
    analysis_ir_schema_version: str
    theorems: list[FormalTheorem] = Field(default_factory=list)
    unresolved: list[UnresolvedItem] = Field(default_factory=list)
    verification: VerificationSummary = Field(default_factory=VerificationSummary)
