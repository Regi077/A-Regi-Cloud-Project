# =============================================================================
#  app.py  --  Cloud Compliance Rule Ingestion Microservice
# =============================================================================
#  Author: Reginald
#  Last updated: 20th June 2025
#
#  DESCRIPTION:
#    - Entry point for the Rule Ingestion microservice.
#    - Handles upload, parsing, extraction, JSON storage, and upsert to Qdrant.
#    - Publishes ingestion status events to RabbitMQ for real-time dashboarding.
#    - Fully self-contained; deployable as a Docker microservice.
#
#  USAGE:
#    - GET /            : Health check endpoint confirming service is running.
#    - POST /ingest-doc : Upload a PDF or text compliance document.
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

# --- Define directories for storing uploads and parsed JSON output ---
UPLOAD_DIR = "uploads"
PARSED_DIR = "parsed_rules"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PARSED_DIR, exist_ok=True)

# --- Initialize Flask app and enable CORS for cross-origin requests ---
app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    """
    Root route for health check.
    Returns a simple success message confirming the service is alive.
    This endpoint prevents 404 errors on the root URL, signaling
    that the service is running and reachable.
    """
    return "Rule Ingestion service is running", 200

@app.route('/ingest-doc', methods=['POST'])
def ingest_doc():
    """
    POST endpoint to receive a compliance document file, process it,
    extract rules using LLM, store results, update Qdrant DB, and publish
    ingestion status events for dashboarding.

    Workflow:
      1. Receive uploaded file and save locally.
      2. Parse document into manageable chunks for LLM input.
      3. Call external LLM service (Ollama/Gemma) to extract rules as JSON.
      4. Save extracted rules JSON for traceability and audit purposes.
      5. Upsert extracted rules into Qdrant vector database for semantic search.
      6. Publish ingestion completion event to RabbitMQ event bus.
      7. Return JSON response with success status and metadata.
    """
    try:
        # Extract file from incoming POST request
        file = request.files['file']
        filename = file.filename
        save_path = os.path.join(UPLOAD_DIR, filename)
        file.save(save_path)

        # Step 1: Parse and chunk document text to prepare for LLM processing
        chunks = parse_doc_to_chunks(save_path)

        # Step 2: Use LLM to extract structured compliance rules from chunks
        rules_json = extract_rules_with_llm(chunks)

        # Step 3: Save the extracted rules as JSON file for audit and traceability
        json_path = save_json(rules_json, filename, PARSED_DIR)

        # Step 4: Insert or update the rules in Qdrant vector database
        qdrant_status = upsert_rules_to_qdrant(rules_json)

        # Step 5: Publish ingestion event with relevant metadata to RabbitMQ
        event_payload = {
            "status": "done",
            "pipeline": "rule-ingestion",
            "file": filename,
            "json_path": json_path,
            "qdrant": qdrant_status
        }
        publish_event("rule.ingestion", event_payload)

        # Step 6: Respond with processing result summary as JSON
        return jsonify({
            "status": "success",
            "file": filename,
            "json_path": json_path,
            "qdrant": qdrant_status
        })

    except Exception as e:
        # Log error (consider publishing an error event here)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(405)
def method_not_allowed(e):
    """
    Handler for 405 Method Not Allowed errors.
    Returns a JSON response explaining allowed methods.
    """
    return jsonify({"error": "Method not allowed", "message": str(e)}), 405

if __name__ == "__main__":
    # Debug mode enabled for development only.
    # Host set to 0.0.0.0 to allow external connections via Docker port mapping.
    app.run(host="0.0.0.0", port=5010, debug=True)

# =============================================================================
#  End of app.py  (Cloud Compliance Rule Ingestion Pipeline)
# =============================================================================
