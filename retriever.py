from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
from utils import read_text_file, chunk_text, keyword_score

@dataclass
class Evidence:
    file: str
    score: int
    snippet: str


def load_documents(folder: Path) -> Dict[str, str]:
    docs = {}
    if not folder.exists():
        return docs
    for path in folder.rglob('*'):
        if path.is_file() and path.suffix.lower() in {'.txt', '.md'}:
            try:
                docs[str(path)] = read_text_file(path)
            except Exception:
                pass
    return docs


def local_search(query: str, docs: Dict[str, str], top_k: int = 4, chunk_size: int = 700, overlap: int = 120) -> List[Evidence]:
    results = []
    for file, content in docs.items():
        for chunk in chunk_text(content, chunk_size, overlap):
            score = keyword_score(query, chunk)
            if score > 0:
                results.append(Evidence(file=file, score=score, snippet=chunk[:300]))
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:top_k]