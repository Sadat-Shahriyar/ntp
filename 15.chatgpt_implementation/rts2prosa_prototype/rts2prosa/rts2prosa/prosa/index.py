from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
import re

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class ProsaDoc:
    doc_id: str
    title: str
    path: str
    text: str


def _read_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() in {".html", ".htm"}:
        soup = BeautifulSoup(raw, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else path.stem
        return title + "\n" + soup.get_text("\n", strip=True)
    return raw


def load_prosa_docs(root: str | Path, chunk_chars: int = 5000) -> list[ProsaDoc]:
    root = Path(root); docs=[]; i=0
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".html",".htm",".md",".txt",".v"}:continue
        text=_read_text(p); title=p.stem
        paras=[x.strip() for x in re.split(r"\n\s*\n",text) if x.strip()]
        buf=""
        for para in paras:
            if buf and len(buf)+len(para)>chunk_chars:
                i+=1; docs.append(ProsaDoc(f"prosa_{i:06d}",title,str(p),buf));buf=""
            buf += ("\n\n" if buf else "")+para
        if buf:
            i+=1;docs.append(ProsaDoc(f"prosa_{i:06d}",title,str(p),buf))
    return docs


class ProsaIndex:
    def __init__(self, docs:list[ProsaDoc]):
        self.docs=docs
        self.vectorizer=TfidfVectorizer(lowercase=True,ngram_range=(1,2),max_features=120000)
        self.matrix=self.vectorizer.fit_transform([d.text for d in docs]) if docs else None

    def search(self, query:str, top_k:int=8):
        if not self.docs:return []
        q=self.vectorizer.transform([query]); scores=cosine_similarity(q,self.matrix)[0]
        ids=scores.argsort()[::-1][:top_k]
        return [(self.docs[i],float(scores[i])) for i in ids if scores[i]>0]
