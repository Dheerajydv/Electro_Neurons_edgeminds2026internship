from typing import List
from ollama_client import get_llm
from retriever import Evidence


def answer_question(question: str, evidences: List[Evidence]) -> str:
    context = '\n\n'.join([f'File: {e.file}\nSnippet: {e.snippet}' for e in evidences]) or 'No evidence found.'
    prompt = (
        'Answer the question using only the evidence. Be concise and cite filenames naturally.\n\n'
        f'Question: {question}\n\nEvidence:\n{context}'
    )
    llm = get_llm()
    if llm is not None:
        try:
            return llm.complete(prompt).text.strip()
        except Exception:
            pass
    if evidences:
        files = ', '.join(sorted(set(e.file for e in evidences)))
        return f'Based on {len(evidences)} evidence snippets, relevant local sources include: {files}.'
    return 'No relevant evidence found in local documents.'