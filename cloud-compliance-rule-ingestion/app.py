# =============================================================================
#  app.py  --  Cloud Compliance Rule Ingestion Microservice
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Entry point for the Rule Ingestion microservice.
#    - Handles upload, parsing, extraction, JSON storage, and upsert to Qdrant.
#    - Publishes ingestion status events to RabbitMQ for real-time dashboarding.
#    - Fully self-contained; deployable as a Docker microservice.
#
#  USAGE:
#    - POST /ingest-doc: Upload a PDF or text compliance document.
#    - The service extracts, chunks, and parses rules using LLMs, stores results,
#      syncs them with Qdrant, and emits status to the event bus.
#
#  PIPELINE STEPS:
#    1. Receive/upload document.
#    2. Parse/chunk document text (parse_utils.py).
#    3. Extract compliance rules via LLM (Ollama/Gemma).
#    4. Save extracted rules as JSON.
#    5. Upsert JSON rules into Qdrant Vector DB.
#    6. Publish result as an event to RabbitMQ ("rule.ingestion" topic).
# =============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from parse_utils import parse_doc_to_chunks, extract_rules_with_llm, save_json
from qdrant_utils import upsert_rules_to_qdrant
from event_bus import publish_event

# --- Directories for uploads and parsed output ---
UPLOAD_DIR = "uploads"
PARSED_DIR = "parsed_rules"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PARSED_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.route('/ingest-doc', methods=['POST'])
def ingest_doc():
    """
    Receives a document file, extracts rules, saves locally,
    pushes to Qdrant, and publishes a pipeline event.
    """
    file = request.files['file']
    filename = file.filename
    save_path = os.path.join(UPLOAD_DIR, filename)
    file.save(save_path)

    # 1. Parse and chunk document for LLM-friendly processing
    chunks = parse_doc_to_chunks(save_path)
    # 2. Extract rules using LLM (Ollama/Gemma via API)
    rules_json = extract_rules_with_llm(chunks)
    # 3. Save parsed rules as JSON for traceability/auditing
    json_path = save_json(rules_json, filename, PARSED_DIR)
    # 4. Upsert extracted rules into Qdrant vector DB (for RAG, etc)
    qdrant_status = upsert_rules_to_qdrant(rules_json)

    # 5. Publish a pipeline event so dashboard and logs update live
    event_payload = {
        "status": "done",
        "pipeline": "rule-ingestion",
        "file": filename,
        "json_path": json_path,
        "qdrant": qdrant_status
    }
    publish_event("rule.ingestion", event_payload)

    # 6. Respond with the full process status
    return jsonify({
        "status": "success",
        "file": filename,
        "json_path": json_path,
        "qdrant": qdrant_status
    })

if __name__ == "__main__":
    # Note: Debug=True is for development only! Use gunicorn for production.
    app.run(port=5010, debug=True)

# =============================================================================
#  End of app.py  (Cloud Compliance Rule Ingestion Pipeline)
# =============================================================================
