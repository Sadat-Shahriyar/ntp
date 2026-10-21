from pathlib import Path
from rts2prosa.prosa.index import load_prosa_docs, ProsaIndex


def test_index(tmp_path: Path):
    (tmp_path / "a.md").write_text("Request bound function bounds cumulative requested work.")
    (tmp_path / "b.md").write_text("Supply bound function lower bounds processor service.")
    idx = ProsaIndex(load_prosa_docs(tmp_path, chunk_chars=1000))
    hits = idx.search("request bound requested work", top_k=1)
    assert hits
    assert hits[0][0].path.endswith("a.md")
