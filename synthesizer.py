from typing import List
from ollama_client import get_llm
from retriever import Evidence

INSUFFICIENT = "The provided evidence is insufficient to fully answer this question."


def answer_question(question: str, evidences: List[Evidence]) -> str:
    if not evidences:
        return INSUFFICIENT

    context_blocks = []
    for i, e in enumerate(evidences, start=1):
        snippet = (e.snippet or "").strip()
        if snippet:
            context_blocks.append(f"[{i}] File: {e.file}\nSnippet: {snippet}")

    if not context_blocks:
        return INSUFFICIENT

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are an evidence-grounded research assistant.

Answer the question using only the evidence below.
Do not use outside knowledge.
Do not invent missing details.
If the evidence supports only part of the answer, provide only the supported part.
If the evidence does not support the answer at all, say exactly:
{INSUFFICIENT}

Rules:
- Be concise and direct.
- Use 3 to 5 short bullet points.
- One claim per bullet.
- Prefer wording that is close to the evidence.
- Do not include explanations that are not directly supported.
- Do not force completeness.
- If support is partial, answer with only supported claims and do not speculate.

Question:
{question}

Evidence:
{context}

Output:
- If supported, return 3 to 5 short bullet points.
- If partially supported, return only the supported bullet points.
- If unsupported, return exactly:
{INSUFFICIENT}
""".strip()

    llm = get_llm()
    if llm is not None:
        try:
            response = llm.complete(prompt).text.strip()
            if response:
                return response
        except Exception:
            pass

    return INSUFFICIENT