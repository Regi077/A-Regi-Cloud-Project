# =============================================================================
#  ollama_client.py  --  LLM Query Utility for Rule Extraction
# =============================================================================
#  Author: Reginald
#  Last updated: 21st June 2025
#
#  PURPOSE:
#    - Provides a simple interface to interact with the Ollama LLM API,
#      specifically the Gemma:2b model, for extracting compliance rules
#      from uploaded documents.
#
#  HOW IT WORKS:
#    - The query_ollama() function sends a prompt to the Ollama server
#      (containerized or native), receives a completion, and returns the response.
#
#  CONFIGURATION:
#    - OLLAMA_URL can be set via environment variable for Docker/host/Cloud.
#      - Defaults to "http://ollama:11434/api/generate" (correct endpoint for Ollama Docker API)
#      - For host/native, set OLLAMA_URL="http://host.docker.internal:11434/api/generate"
# =============================================================================

import requests
import os

# Base URL for Ollama API endpoint.
# Use '/api/generate' as required by current Ollama Docker API (v0.9.2+)
OLLAMA_URL = os.getenv(
    "OLLAMA_URL", "http://ollama:11434/api/generate"
)  #: Use Docker Compose service name by default

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
        "model": "gemma:2b",
        "prompt": prompt,              # The text to analyze or answer
        "stream": False,               # Set to False for full (non-streaming) response
        "temperature": 0.1             # Low temperature for deterministic output
    }

    # Make POST request to Ollama API endpoint
    resp = requests.post(OLLAMA_URL, json=data)

    # Raise exception for HTTP error codes (4xx, 5xx)
    resp.raise_for_status()

    # Extract the 'response' field from JSON payload, return empty string if missing
    return resp.json().get("response", "")

# =============================================================================
#  End of ollama_client.py (LLM integration for compliance rule extraction)
# =============================================================================
