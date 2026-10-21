from __future__ import annotations

import re
from rts2prosa.document.parser import MarkdownChunk
from rts2prosa.ir.base import EvidenceSpan


def find_quote(source: str, quote: str):
    q = quote.strip()
    if q in source:
        s = source.index(q); return s, s + len(q)
    tokens = [x for x in re.split(r"\s+", q) if x]
    if not tokens:
        return None
    pat = r"\s+".join(re.escape(x) for x in tokens)
    m = re.search(pat, source, flags=re.S)
    return None if m is None else (m.start(), m.end())


def verify_quote(chunk: MarkdownChunk, quote: str) -> EvidenceSpan | None:
    loc = find_quote(chunk.text, quote)
    if loc is None:
        return None
    s, e = loc
    before, matched = chunk.text[:s], chunk.text[s:e]
    l0 = before.count("\n")
    l1 = l0 + matched.count("\n")
    return EvidenceSpan(chunk_id=chunk.chunk_id, section=chunk.section, line_start=chunk.line_start + l0, line_end=chunk.line_start + l1, quote=matched)
