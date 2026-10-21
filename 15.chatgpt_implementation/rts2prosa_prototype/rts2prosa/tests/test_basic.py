from rts2prosa.common.expressions import ExprNode, collect_symbols
from rts2prosa.document.parser import chunk_markdown
from rts2prosa.document.theory import build_theory_graph


def test_expr():
    x=ExprNode(kind="symbol",name="x")
    y=ExprNode(kind="symbol",name="y")
    e=ExprNode(kind="op",namespace="core",op="le",args=[x,y])
    assert collect_symbols(e)=={"x","y"}


def test_markdown():
    md="# Title\n\n## Model\n\nWe consider tasks.\n\nTheorem 1. X.\n"
    chunks=chunk_markdown(md,1000)
    assert chunks
    graph=build_theory_graph(chunks)
    assert any(n.kind=="theorem" for n in graph.nodes)
