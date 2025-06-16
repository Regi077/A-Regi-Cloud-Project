# This is the main entry point for the Flask application.
# It sets up the necessary directories, initializes the Flask app,
# and defines the endpoint for document ingestion.
# The endpoint handles file uploads, processes the document to extract rules,
# saves the extracted rules as JSON, and upserts them to Qdrant.
# The application runs on port 5010 and is set to debug mode for development.


from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from parse_utils import parse_doc_to_chunks, extract_rules_with_llm, save_json
from qdrant_utils import upsert_rules_to_qdrant
# Ensure necessary directories exist

UPLOAD_DIR = "uploads"
PARSED_DIR = "parsed_rules"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PARSED_DIR, exist_ok=True)


app = Flask(__name__)
CORS(app)

@app.route('/ingest-doc', methods=['POST'])
def ingest_doc():
    file = request.files['file']
    filename = file.filename
    save_path = os.path.join(UPLOAD_DIR, filename)
    file.save(save_path)

    # 1. Parse and chunk doc
    chunks = parse_doc_to_chunks(save_path)
    # 2. LLM (Ollama) rule extraction
    rules_json = extract_rules_with_llm(chunks)
    # 3. Save JSON locally
    json_path = save_json(rules_json, filename, PARSED_DIR)
    # 4. Upsert rules to Qdrant
    qdrant_status = upsert_rules_to_qdrant(rules_json)
    return jsonify({
        "status": "success",
        "file": filename,
        "json_path": json_path,
        "qdrant": qdrant_status
    })

if __name__ == "__main__":
    app.run(port=5010, debug=True)

