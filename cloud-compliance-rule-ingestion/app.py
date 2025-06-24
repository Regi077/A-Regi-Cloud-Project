# =============================================================================
#  app.py  --  Cloud Compliance Rule Ingestion Microservice
# =============================================================================
#  Author: Reginald
#  Last updated: 21st June 2025
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

from flask import Flask, request, jsonify, send_from_directory  # Added send_from_directory for favicon
from flask_cors import CORS
import os
import traceback  # <-- ADDED for full error tracing
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

# -----------------------------------------------------------------------------
# Serve favicon.ico from /static to eliminate browser 404 log spam
# -----------------------------------------------------------------------------
@app.route('/favicon.ico')
def favicon():
    """
    Serves the favicon.ico file from the static directory.
    Prevents browser tab 404s and log noise for missing favicon.
    """
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

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
        # Defensive file check for robust error handling
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part in the request"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"}), 400

        filename = file.filename
        save_path = os.path.join(UPLOAD_DIR, filename)
        file.save(save_path)

        # Step 1: Parse and chunk document text to prepare for LLM processing
        chunks = parse_doc_to_chunks(save_path)

        # Step 2: Use LLM to extract structured compliance rules from chunks
        rules_json = extract_rules_with_llm(chunks)

        # --- DEBUGGING SECTION: Print rule extraction results ---
        print(f"[DEBUG] Number of rules extracted: {len(rules_json)}")
        print(f"[DEBUG] Extracted rules sample: {rules_json[:1]}")
        # -------------------------------------------------------

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

        # Optional: Log to stdout for Docker container logs
        print(f"[INFO] File '{filename}' ingested successfully and stored at '{json_path}'.")

        # Step 6: Respond with processing result summary as JSON
        return jsonify({
            "status": "success",
            "file": filename,
            "json_path": json_path,
            "qdrant": qdrant_status
        })

    except Exception as e:
        # Print detailed error log for container debugging
        print("[ERROR] Exception in /ingest-doc:", str(e))
        traceback.print_exc()
        # Optionally publish error event here
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
