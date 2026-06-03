import os  # Used to read environment variables
from functools import lru_cache  # Cache the model instance so it is created once

try:
    # Try to import the Ollama client from llama-index
    from llama_index.llms.ollama import Ollama
except Exception:
    # If the package is missing, disable LLM support gracefully
    Ollama = None


@lru_cache(maxsize=1)
def get_llm():
    # If Ollama is not installed, return None so the rest of the code can fallback
    if Ollama is None:
        return None
    # Read model and server settings from environment variables
    model_name = os.getenv('MODEL_NAME', 'llama3.2:1b')
    ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    try:
        # Create and return the local LLM client
        return Ollama(model=model_name, base_url=ollama_url, request_timeout=120.0)
    except Exception:
        # Return None if client creation fails for any reason
        return None