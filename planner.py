import json  # Used to parse the model's JSON output
from typing import List  # Type hint for a list of strings
from ollama_client import get_llm  # Access the optional local LLM


def plan_subquestions(topic: str, max_subquestions: int = 5) -> List[str]:
    # Prompt the model to generate a compact set of sub-questions
    prompt = (
        'Create 3 to 5 short sub-questions for this research topic. '
        'Return only a JSON array of strings.\n\n'
        f'Topic: {topic}'
    )
    # Get the local LLM if available
    llm = get_llm()
    # Try model-based planning first
    if llm is not None:
        try:
            # Ask the model for a JSON list of sub-questions
            response = llm.complete(prompt).text.strip()
            # Convert the response to a Python list
            arr = json.loads(response)
            # Ensure the result is a non-empty list
            if isinstance(arr, list) and arr:
                # Normalize text and limit the count
                return [str(x).strip() for x in arr][:max_subquestions]
        except Exception:
            # Fall back to rule-based questions if the model fails
            pass
    # Default fallback questions used when no model output is available
    return [
        f'What is the main goal of {topic}?',
        f'What are the key components of {topic}?',
        f'How should {topic} be implemented locally?',
        f'What are the edge deployment constraints for {topic}?',
    ][:max_subquestions]