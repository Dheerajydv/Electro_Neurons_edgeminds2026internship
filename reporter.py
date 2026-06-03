from pathlib import Path
from typing import Dict, List
from retriever import Evidence


def compile_report(topic: str, subquestions: List[str], answers: Dict[str, str]) -> str:
    lines = [f'# Research Report: {topic}', '']
    for q in subquestions:
        lines.append(f'## {q}')
        lines.append(answers.get(q, ''))
        lines.append('')
    return '\n'.join(lines).strip() + '\n'


def save_report(report: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / 'final_report.md'
    path.write_text(report, encoding='utf-8')
    return path


def save_evidence(evidence_map: Dict[str, List[Evidence]], output_dir: Path) -> Path:
    import json
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / 'evidence.json'
    serializable = {q: [e.__dict__ for e in evs] for q, evs in evidence_map.items()}
    path.write_text(json.dumps(serializable, indent=2), encoding='utf-8')
    return path