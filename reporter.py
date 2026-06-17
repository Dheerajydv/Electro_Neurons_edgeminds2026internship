from pathlib import Path
from typing import Dict, List
import json
from retriever import Evidence

def compile_report(topic: str, subquestions: List[str], answers: Dict[str, str]) -> str:
    lines = [
        f"# Research Report: {topic}",
        "",
        "## Overview",
        f"This report was generated automatically for the topic: **{topic}**.",
        "",
    ]

    for q in subquestions:
        lines.append(f"## {q}")
        lines.append(answers.get(q, "No answer generated."))
        lines.append("")

    return "\n".join(lines).strip() + "\n"

def save_report(report: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "final_report.md"
    path.write_text(report, encoding="utf-8")
    return path

def save_evidence(evidence_map: Dict[str, List[Evidence]], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "evidence.json"

    serializable = {
        q: [e.__dict__ for e in evidences]
        for q, evidences in evidence_map.items()
    }

    path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")
    return path