from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator

CORE_OPERATIONS = {
    "add", "sub", "mul", "div", "ceil", "floor", "ceil_div", "floor_div",
    "sum", "max", "min", "eq", "neq", "lt", "le", "gt", "ge",
    "and", "or", "not", "implies", "iff", "in", "subset", "piecewise", "case"
}


class ExprNode(BaseModel):
    kind: Literal["symbol", "literal", "call", "op", "quantifier"]
    name: Optional[str] = None
    value: Optional[str] = None
    args: list["ExprNode"] = Field(default_factory=list)
    namespace: Optional[Literal["core", "rts", "paper"]] = None
    op: Optional[str] = None
    quantifier: Optional[Literal["forall", "exists"]] = None
    variable: Optional[str] = None
    domain: Optional["ExprNode"] = None
    body: Optional["ExprNode"] = None

    @model_validator(mode="after")
    def validate_node(self):
        if self.kind == "symbol" and not self.name:
            raise ValueError("symbol requires name")
        if self.kind == "literal" and self.value is None:
            raise ValueError("literal requires value")
        if self.kind == "call" and not self.name:
            raise ValueError("call requires function name")
        if self.kind == "op":
            if not self.op or not self.namespace:
                raise ValueError("op requires namespace and op")
            if self.namespace == "core" and self.op not in CORE_OPERATIONS:
                raise ValueError(f"unknown core operation: {self.op}")
        if self.kind == "quantifier":
            if not self.quantifier or not self.variable or self.body is None:
                raise ValueError("quantifier requires quantifier, variable, body")
        return self


def collect_symbols(expr: ExprNode | None) -> set[str]:
    if expr is None:
        return set()
    out: set[str] = set()
    if expr.kind == "symbol" and expr.name:
        out.add(expr.name)
    for a in expr.args:
        out |= collect_symbols(a)
    if expr.domain:
        out |= collect_symbols(expr.domain)
    if expr.body:
        out |= collect_symbols(expr.body)
    if expr.kind == "quantifier" and expr.variable:
        out.discard(expr.variable)
    return out


def collect_calls(expr: ExprNode | None) -> set[str]:
    if expr is None:
        return set()
    out: set[str] = set()
    if expr.kind == "call" and expr.name:
        out.add(expr.name)
    for a in expr.args:
        out |= collect_calls(a)
    if expr.domain:
        out |= collect_calls(expr.domain)
    if expr.body:
        out |= collect_calls(expr.body)
    return out

ExprNode.model_rebuild()
