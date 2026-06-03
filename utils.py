import re
from pathlib import Path
from typing import List


def read_text_file(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> List[str]:
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return []
    chunks, i = [], 0
    while i < len(text):
        chunks.append(text[i:i + chunk_size])
        i += max(1, chunk_size - overlap)
    return chunks


def keyword_score(query: str, text: str) -> int:
    q = [w.lower() for w in re.findall(r'[a-zA-Z0-9]+', query) if len(w) > 2]
    t = text.lower()
    return sum(t.count(w) for w in q)


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)