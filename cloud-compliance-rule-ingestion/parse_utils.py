# =============================================================================
#  parse_utils.py  --  Compliance Document Parsing & LLM Rule Extraction Utility
# =============================================================================
#  Author: Reginald
#  Last updated: 24th June 2025 (prompt and LLM output normalization improvements)
#
#  DESCRIPTION:
#    - Handles document reading (PDF or text), chunking, LLM-based extraction,
#      and saving of compliance rules as JSON.
#
#  KEY FUNCTIONS:
#    - parse_doc_to_chunks(filepath, chunk_size): Reads & chunks document text.
#    - extract_rules_with_llm(chunks): Sends each chunk to LLM for rule extraction.
#    - save_json(data, filename, outdir): Saves rules to .json file in given directory.
#
#  DEPENDENCIES:
#    - PyPDF2: For reading PDF documents.
#    - ollama_client.py: Handles the actual LLM API calls.
# =============================================================================

import PyPDF2
import os
import json
from ollama_client import query_ollama

# ------------------------------------------------------------
#  parse_doc_to_chunks
# ------------------------------------------------------------
def parse_doc_to_chunks(filepath, chunk_size=700):
    """
    Reads a PDF or text file and splits its content into manageable text chunks.
    This helps avoid LLM token/input limits.

    Args:
        filepath (str): Path to the input document (PDF or .txt).
        chunk_size (int): Size of each chunk in characters (default 700).

    Returns:
        list[str]: List of text chunks.
    """
    text = ""
    if filepath.endswith(".pdf"):
        # Parse PDF document (extract all text)
        with open(filepath, "rb") as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                text += page.extract_text() or ""
    else:
        # Parse plain text file
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    # Chunk the text into overlapping/non-overlapping pieces
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ------------------------------------------------------------
#  extract_rules_with_llm
# ------------------------------------------------------------
def extract_rules_with_llm(chunks):
    """
    Uses the Ollama LLM to extract compliance rules from each text chunk.
    Robust prompt engineering, output cleanup, and full normalization logic.

    Args:
        chunks (list[str]): Chunks of text from the document.

    Returns:
        list[dict]: Aggregated list of all extracted rules (as Python dicts).

    Note:
        - Handles all common LLM issues: markdown code block wrappers, "json" hints, dict/list/string responses.
        - Logs every LLM output for transparency and troubleshooting.
        - Ensures output is always a list of dicts, no matter how LLM responds.
    """
    all_rules = []
    for chunk in chunks:
        # Strong, explicit prompt: Force LLM to return list of dicts only.
        prompt = (
            "Extract all compliance rules from the following text. "
            "Respond ONLY with a JSON array of objects. Each object must be a rule in the format: "
            '[{"rule": "..."}]. If there is only one rule, still return as an array of objects. '
            "Do NOT return a list of strings or commentary.\n\n"
            f"Text:\n{chunk}"
        )
        response = query_ollama(prompt)
        print("LLM raw output:", repr(response))

        # --- CLEANUP: Remove markdown code block markers and other LLM wrappers ---
        cleaned = response.strip()
        # Remove triple backticks and any optional 'json' marker
        if cleaned.startswith("```"):
            cleaned = cleaned.lstrip("`").strip()
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
        cleaned = cleaned.strip("`").strip()

        # --- LLM Output Normalization Logic (Handles all possible formats) ---
        try:
            parsed = json.loads(cleaned)
            rules_list = []

            # CASE 1: List of dicts (ideal format)
            if isinstance(parsed, list):
                rules_list = [r for r in parsed if isinstance(r, dict) and r]
            # CASE 2: Dict with "rules" key ({"rules": [...]})
            elif isinstance(parsed, dict) and "rules" in parsed and isinstance(parsed["rules"], list):
                rules_list = [r for r in parsed["rules"] if isinstance(r, dict) and r]
            # CASE 3: Dict with "rule" key (single rule as dict)
            elif isinstance(parsed, dict) and "rule" in parsed:
                rules_list = [parsed]
            # CASE 4: String response (very rare, last fallback)
            elif isinstance(parsed, str):
                rules_list = [{"rule": parsed}]
            # ELSE: Unknown structure, print for debug
            else:
                print("LLM output not recognized, skipping:", parsed)

            all_rules.extend(rules_list)

        except Exception as e:
            print("JSON parsing failed for chunk:", e)
            continue
    return all_rules

# ------------------------------------------------------------
#  save_json
# ------------------------------------------------------------
def save_json(data, filename, outdir):
    """
    Saves the given data as a pretty-printed JSON file in the specified directory.

    Args:
        data (dict or list): Data to save.
        filename (str): Base name for output file (will be .json).
        outdir (str): Output directory path.

    Returns:
        str: Full path to the saved JSON file.
    """
    json_path = os.path.join(outdir, filename + ".json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return json_path

# =============================================================================
#  End of parse_utils.py (Handles parsing, LLM extraction, and JSON saving)
# =============================================================================
