# =============================================================================
#  ollama_client.py  --  LLM Query Utility for Rule Extraction
# =============================================================================
#  Author: Reginald
#  Last updated: 24th June 2025  (robust error handling, validation)
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
#      - Defaults to "http://ollama:11434/api/generate" (Ollama Docker API)
#      - For host/native, set OLLAMA_URL="http://host.docker.internal:11434/api/generate"
# =============================================================================

import requests
import os

# Base URL for Ollama API endpoint (Docker Compose service name by default)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/generate")

def query_ollama(prompt):
    """
    Sends a text prompt to the Ollama LLM API and retrieves the model's response.

    Args:
        prompt (str): The prompt or question to send to the LLM.

    Returns:
        str: The LLM's textual response (usually JSON-formatted compliance rules).

    Raises:
        RuntimeError: For API connection, HTTP, or JSON errors.

    Usage:
        rules_json = query_ollama("Extract all NIST security requirements...")
    """
    data = {
        "model": "gemma:2b",
        "prompt": prompt,              # The text to analyze or answer
        "stream": False,               # Set to False for full (non-streaming) response
        "temperature": 0.1             # Low temperature for deterministic output
    }

    try:
        resp = requests.post(OLLAMA_URL, json=data, timeout=120)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Log detailed network or HTTP errors
        print("[ERROR] Ollama API connection/request failed:", e)
        raise RuntimeError(f"Ollama API request failed: {e}")

    # Try to parse JSON and validate structure
    try:
        resp_json = resp.json()
    except Exception as e:
        print("[ERROR] Ollama API returned invalid JSON:", e)
        print("Raw response:", resp.text)
        raise RuntimeError(f"Ollama API did not return valid JSON: {e}")

    if "response" not in resp_json or not resp_json["response"].strip():
        # Log missing/empty responses for troubleshooting
        print("[ERROR] Ollama API response missing 'response' field or is empty.")
        print("Full API response:", resp_json)
        raise RuntimeError("Ollama API response missing or empty.")

    return resp_json["response"]

# =============================================================================
#  End of ollama_client.py (LLM integration for compliance rule extraction)
# =============================================================================
