# =============================================================================
#  ollama_client.py  --  LLM Query Utility for Rule Extraction
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  PURPOSE:
#    - Provides a simple interface to interact with the Ollama LLM API,
#      specifically the Gemma:2b model, for extracting compliance rules
#      from uploaded documents.
#
#  HOW IT WORKS:
#    - The query_ollama() function sends a prompt to the local Ollama server,
#      receives a text-based completion, and returns the model's response.
#
#  DEPENDENCIES:
#    - Ollama must be running at the expected URL and port (http://localhost:11434)
#    - The Gemma:2b model must be available in the Ollama server.
# =============================================================================

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"   # Local Ollama API endpoint

def query_ollama(prompt):
    """
    Sends a text prompt to the Ollama LLM API and retrieves the model's response.

    Args:
        prompt (str): The prompt or question to send to the LLM.

    Returns:
        str: The LLM's textual response (usually JSON-formatted compliance rules).

    Raises:
        requests.HTTPError: If the Ollama API is unreachable or returns an error.

    Usage:
        rules_json = query_ollama("Extract all NIST security requirements...")
    """
    data = {
        "model": "gemma:2b",      # Model name (must match your Ollama setup)
        "prompt": prompt,         # The text to analyze or answer
        "stream": False,          # Set to False for full (non-streaming) response
        "temperature": 0.1        # Low temp for deterministic, reproducible output
    }
    resp = requests.post(OLLAMA_URL, json=data)
    resp.raise_for_status()       # Raise error if Ollama is not reachable
    return resp.json().get("response", "")

# =============================================================================
#  End of ollama_client.py (LLM integration for compliance rule extraction)
# =============================================================================
