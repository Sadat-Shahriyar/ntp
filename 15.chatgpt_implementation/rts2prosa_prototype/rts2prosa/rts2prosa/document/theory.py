from __future__ import annotations

import re
from typing import Literal
from pydantic import BaseModel, Field

from rts2prosa.document.parser import MarkdownChunk
from rts2prosa.common.text import stable_id


class TheoryNode(BaseModel):
    id: str
    kind: Literal["definition", "assumption", "lemma", "theorem", "proof", "equation", "section", "other"]
    title: str
    section: str
    chunk_id: str
    text: str
    line_start: int
    line_end: int


class TheoryEdge(BaseModel):
    source: str
    target: str
    relation: Literal["contains", "mentions", "depends_on", "proved_by"]
    confidence: float = 1.0


class TheoryGraph(BaseModel):
    nodes: list[TheoryNode] = Field(default_factory=list)
    edges: list[TheoryEdge] = Field(default_factory=list)


DECL_RE = re.compile(r"\b(Definition|Lemma|Theorem|Proposition|Corollary|Assumption)\s*([0-9A-Za-z_.-]*)", re.I)
EQ_RE = re.compile(r"\$\$.*?\$\$", re.S)


def build_theory_graph(chunks: list[MarkdownChunk]) -> TheoryGraph:
    nodes: list[TheoryNode] = []
    for ch in chunks:
        sid = stable_id("sec", ch.section, ch.chunk_id)
        nodes.append(TheoryNode(id=sid, kind="section", title=ch.section, section=ch.section, chunk_id=ch.chunk_id, text=ch.text, line_start=ch.line_start, line_end=ch.line_end))
        for m in DECL_RE.finditer(ch.text):
            word, label = m.group(1).lower(), (m.group(2) or "").strip()
            kind = "theorem" if word in {"theorem", "proposition", "corollary"} else word
            nid = stable_id(kind, ch.chunk_id, str(m.start()), label)
            snippet = ch.text[m.start():].split("\n\n", 1)[0]
            nodes.append(TheoryNode(id=nid, kind=kind, title=f"{m.group(1)} {label}".strip(), section=ch.section, chunk_id=ch.chunk_id, text=snippet, line_start=ch.line_start + ch.text[:m.start()].count("\n"), line_end=ch.line_start + ch.text[:m.start()+len(snippet)].count("\n")))
        for j, m in enumerate(EQ_RE.finditer(ch.text)):
            nid = stable_id("eq", ch.chunk_id, str(j), m.group(0))
            nodes.append(TheoryNode(id=nid, kind="equation", title=f"Equation {j+1}", section=ch.section, chunk_id=ch.chunk_id, text=m.group(0), line_start=ch.line_start + ch.text[:m.start()].count("\n"), line_end=ch.line_start + ch.text[:m.end()].count("\n")))
    # conservative edges: section contains same-chunk declarations/equations
    edges: list[TheoryEdge] = []
    section_by_chunk = {n.chunk_id: n for n in nodes if n.kind == "section"}
    for n in nodes:
        if n.kind != "section" and n.chunk_id in section_by_chunk:
            edges.append(TheoryEdge(source=section_by_chunk[n.chunk_id].id, target=n.id, relation="contains"))
    return TheoryGraph(nodes=nodes, edges=edges)
