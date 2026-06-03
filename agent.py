from config import Config  # Load runtime configuration values
from retriever import load_documents, local_search  # Document loading and search utilities
from planner import plan_subquestions  # Generate sub-questions using the planner
from synthesizer import answer_question  # Produce answers from retrieved evidence
from reporter import compile_report, save_report, save_evidence  # Build and save report artifacts
from utils import ensure_dir  # Create folders when needed


def run_agent(topic: str) -> str:
    # Read configuration values from environment defaults
    cfg = Config()
    # Ensure the output directory exists before writing files
    ensure_dir(cfg.output_dir)
    # Load all local documents from the configured documents folder
    docs = load_documents(cfg.documents_dir)
    # Ask the planner to break the topic into smaller questions
    subquestions = plan_subquestions(topic, cfg.max_subquestions)
    # Prepare containers for final answers and evidence
    answers = {}
    evidence_map = {}
    # Process each sub-question one by one
    for q in subquestions:
        # Search the local documents for relevant chunks
        ev = local_search(q, docs, top_k=cfg.top_k, chunk_size=cfg.chunk_size, overlap=cfg.overlap)
        # Store evidence for later export
        evidence_map[q] = ev
        # Generate a concise answer from the evidence
        answers[q] = answer_question(q, ev)
    # Compile the per-question answers into a final report string
    report = compile_report(topic, subquestions, answers)
    # Save the final markdown report to disk
    save_report(report, cfg.output_dir)
    # Save all evidence details to a JSON file for traceability
    save_evidence(evidence_map, cfg.output_dir)
    # Return the report so main.py can print it
    return report