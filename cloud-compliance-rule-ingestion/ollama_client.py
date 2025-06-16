import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_ollama(prompt):
    data = {
        "model": "gemma:2b",
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1
    }
    resp = requests.post(OLLAMA_URL, json=data)
    resp.raise_for_status()
    return resp.json().get("response", "")
