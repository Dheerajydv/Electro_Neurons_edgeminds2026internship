import re
from pathlib import Path
from typing import List

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()

def tokenize(text: str) -> List[str]:
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> List[str]:
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    step = max(1, chunk_size - overlap)

    while start < len(text):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
        start += step

    return chunks

def keyword_score(query: str, chunk: str) -> int:
    q_tokens = tokenize(query)
    c_text = normalize_text(chunk)
    return sum(1 for token in q_tokens if token in c_text)