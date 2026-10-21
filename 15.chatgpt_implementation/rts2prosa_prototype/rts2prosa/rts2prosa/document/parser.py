from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import re

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


@dataclass
class MarkdownChunk:
    chunk_id: str
    section: str
    heading_path: List[str]
    text: str
    line_start: int
    line_end: int


def parse_markdown_sections(text: str):
    lines = text.splitlines()
    stack: list[str] = []
    sections = []
    cur_lines: list[str] = []
    cur_heading = "ROOT"
    start = 1

    def flush(end_line: int):
        nonlocal cur_lines
        if cur_lines:
            sections.append({
                "heading": cur_heading,
                "heading_path": list(stack),
                "lines": list(cur_lines),
                "line_start": start,
                "line_end": end_line,
            })
        cur_lines = []

    for lineno, line in enumerate(lines, 1):
        m = HEADING_RE.match(line)
        if m:
            flush(lineno - 1)
            level, title = len(m.group(1)), m.group(2).strip()
            stack[:] = stack[:level - 1]
            while len(stack) < level - 1:
                stack.append("")
            stack.append(title)
            cur_heading = title
            start = lineno + 1
        else:
            cur_lines.append(line)
    flush(len(lines))
    return sections


def _blocks(lines: list[str]) -> list[str]:
    blocks, buf = [], []
    for line in lines:
        if not line.strip():
            if buf:
                blocks.append("\n".join(buf)); buf = []
        else:
            buf.append(line)
    if buf:
        blocks.append("\n".join(buf))
    return blocks


def chunk_markdown(text: str, max_chars: int = 6000) -> list[MarkdownChunk]:
    out: list[MarkdownChunk] = []
    n = 0
    for sec in parse_markdown_sections(text):
        buf: list[str] = []
        chars = 0
        cursor = sec["line_start"]
        chunk_start = cursor
        for block in _blocks(sec["lines"]):
            if buf and chars + len(block) > max_chars:
                t = "\n\n".join(buf); n += 1
                lc = t.count("\n") + 1
                out.append(MarkdownChunk(f"chunk_{n:04d}", sec["heading"], sec["heading_path"], t, chunk_start, chunk_start + lc - 1))
                chunk_start = cursor; buf = []; chars = 0
            buf.append(block); chars += len(block); cursor += block.count("\n") + 2
        if buf:
            t = "\n\n".join(buf); n += 1
            lc = t.count("\n") + 1
            out.append(MarkdownChunk(f"chunk_{n:04d}", sec["heading"], sec["heading_path"], t, chunk_start, chunk_start + lc - 1))
    return out


def read_and_chunk(path: str | Path, max_chars: int = 6000) -> tuple[str, list[MarkdownChunk]]:
    text = Path(path).read_text(encoding="utf-8")
    return text, chunk_markdown(text, max_chars=max_chars)
