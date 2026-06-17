from functools import lru_cache
from config import Config

try:
    from llama_index.llms.ollama import Ollama
except Exception:
    Ollama = None

@lru_cache(maxsize=1)
def get_llm():
    if Ollama is None:
        return None

    cfg = Config()

    try:
        return Ollama(
            model=cfg.model_name,
            base_url=cfg.ollama_url,
            request_timeout=120.0
        )
    except Exception:
        return None