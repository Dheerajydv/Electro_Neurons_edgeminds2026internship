from dataclasses import dataclass
from pathlib import Path
import os

@dataclass
class Config:
    model_name: str = os.getenv("MODEL_NAME", "llama3.2:1b")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    documents_dir: Path = Path(os.getenv("DOCUMENTS_DIR", "documents"))
    output_dir: Path = Path(os.getenv("OUTPUT_DIR", "output"))
    top_k: int = int(os.getenv("TOP_K", "4"))
    max_subquestions: int = int(os.getenv("MAX_SUBQUESTIONS", "5"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "700"))
    overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    