import PyPDF2
import os
import json
from ollama_client import query_ollama

# Function to parse a document and extract compliance rules using an LLM

def parse_doc_to_chunks(filepath, chunk_size=700):
    text = ""
    if filepath.endswith(".pdf"):
        with open(filepath, "rb") as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                text += page.extract_text() or ""
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    # Simple chunking
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def extract_rules_with_llm(chunks):
    all_rules = []
    for chunk in chunks:
        prompt = f"Extract all compliance rules from this text as JSON list of rules: {chunk}"
        response = query_ollama(prompt)
        # Parse response, assuming response is valid JSON list (mock/demo only)
        try:
            rules = json.loads(response)
            all_rules.extend(rules)
        except Exception:
            continue
    return all_rules

def save_json(data, filename, outdir):
    json_path = os.path.join(outdir, filename + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return json_path

