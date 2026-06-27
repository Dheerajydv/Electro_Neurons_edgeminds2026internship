from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple
import math
import re

from utils import read_text_file, chunk_text


@dataclass
class Evidence:
    file: str
    score: float
    snippet: str


_WORD_RE = re.compile(r"\b[a-z0-9]+\b", re.IGNORECASE)


def normalize(text: str) -> List[str]:
    return _WORD_RE.findall((text or "").lower())


def load_documents(folder: Path) -> Dict[str, str]:
    docs = {}

    if not folder.exists():
        return docs

    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".txt", ".md"}:
            try:
                text = read_text_file(path)
                if text and text.strip():
                    docs[str(path)] = text
            except Exception:
                pass

    return docs


def smart_chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
    if not paragraphs:
        return chunk_text(text, chunk_size, overlap)

    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= chunk_size:
            current = f"{current}\n\n{para}".strip()
        else:
            if current:
                chunks.append(current)
            current = para

    if current:
        chunks.append(current)

    if len(chunks) <= 1:
        return chunk_text(text, chunk_size, overlap)

    merged = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            merged.append(chunk)
        else:
            prev_tail = chunks[i - 1][-overlap:] if overlap > 0 else ""
            merged.append((prev_tail + "\n" + chunk).strip())

    return merged


def build_corpus_chunks(
    docs: Dict[str, str],
    chunk_size: int = 700,
    overlap: int = 120,
) -> List[Tuple[str, str, List[str]]]:
    corpus = []
    for file, content in docs.items():
        chunks = smart_chunk_text(content, chunk_size=chunk_size, overlap=overlap)
        for chunk in chunks:
            tokens = normalize(chunk)
            if tokens:
                corpus.append((file, chunk, tokens))
    return corpus


def compute_idf(corpus_tokens: List[List[str]]) -> Dict[str, float]:
    df = {}
    n_docs = len(corpus_tokens)

    for tokens in corpus_tokens:
        for token in set(tokens):
            df[token] = df.get(token, 0) + 1

    idf = {}
    for token, freq in df.items():
        idf[token] = math.log(1 + (n_docs - freq + 0.5) / (freq + 0.5))
    return idf


def bm25_score(
    query_tokens: List[str],
    doc_tokens: List[str],
    idf: Dict[str, float],
    avgdl: float,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    if not query_tokens or not doc_tokens:
        return 0.0

    score = 0.0
    doc_len = len(doc_tokens)
    tf = {}

    for tok in doc_tokens:
        tf[tok] = tf.get(tok, 0) + 1

    for tok in query_tokens:
        if tok not in tf:
            continue
        freq = tf[tok]
        tok_idf = idf.get(tok, 0.0)
        denom = freq + k1 * (1 - b + b * (doc_len / avgdl if avgdl > 0 else 1))
        score += tok_idf * ((freq * (k1 + 1)) / denom)

    return score


def keyword_coverage_score(query_tokens: List[str], doc_tokens: List[str]) -> float:
    if not query_tokens or not doc_tokens:
        return 0.0
    qset = set(query_tokens)
    dset = set(doc_tokens)
    overlap = len(qset & dset)
    return overlap / max(len(qset), 1)


def phrase_bonus(query: str, chunk: str) -> float:
    query = (query or "").strip().lower()
    chunk_l = (chunk or "").lower()
    if not query or not chunk_l:
        return 0.0

    bonus = 0.0
    if query in chunk_l:
        bonus += 1.5

    query_words = query.split()
    if len(query_words) >= 2:
        for i in range(len(query_words) - 1):
            phrase = f"{query_words[i]} {query_words[i+1]}"
            if phrase in chunk_l:
                bonus += 0.3

    return bonus


def rerank_score(query: str, query_tokens: List[str], chunk: str, doc_tokens: List[str], base_score: float) -> float:
    coverage = keyword_coverage_score(query_tokens, doc_tokens)
    bonus = phrase_bonus(query, chunk)

    starts_strong = 0.15 if any(tok in normalize(chunk[:220]) for tok in query_tokens) else 0.0
    length_penalty = 0.0
    if len(chunk) < 120:
        length_penalty -= 0.2
    elif len(chunk) > 1800:
        length_penalty -= 0.15

    return base_score + (coverage * 2.0) + bonus + starts_strong + length_penalty


def local_search(
    query: str,
    docs: Dict[str, str],
    top_k: int = 4,
    candidate_k: int = 10,
    chunk_size: int = 700,
    overlap: int = 120,
    snippet_chars: int = 900,
) -> List[Evidence]:
    query_tokens = normalize(query)
    if not query_tokens or not docs:
        return []

    corpus = build_corpus_chunks(docs, chunk_size=chunk_size, overlap=overlap)
    if not corpus:
        return []

    corpus_tokens = [tokens for _, _, tokens in corpus]
    idf = compute_idf(corpus_tokens)
    avgdl = sum(len(tokens) for tokens in corpus_tokens) / max(len(corpus_tokens), 1)

    scored = []
    for file, chunk, tokens in corpus:
        base = bm25_score(query_tokens, tokens, idf, avgdl)
        if base <= 0:
            continue
        scored.append((file, chunk, tokens, base))

    if not scored:
        return []

    scored.sort(key=lambda x: x[3], reverse=True)
    candidates = scored[:max(candidate_k, top_k)]

    reranked = []
    for file, chunk, tokens, base in candidates:
        final_score = rerank_score(query, query_tokens, chunk, tokens, base)
        reranked.append(
            Evidence(
                file=file,
                score=final_score,
                snippet=chunk[:snippet_chars].strip()
            )
        )

    reranked.sort(key=lambda x: x.score, reverse=True)

    deduped: List[Evidence] = []
    seen = set()
    for ev in reranked:
        key = (ev.file, ev.snippet[:200])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(ev)
        if len(deduped) >= top_k:
            break

    return deduped