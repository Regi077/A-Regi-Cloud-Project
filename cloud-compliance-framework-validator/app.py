# =============================================================================
#  app.py  --  Cloud Compliance Framework Validator Microservice
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - This Flask app receives Infrastructure-as-Code (IaC) files (YAML or Terraform)
#      and a compliance framework name from the UI or API Gateway.
#    - It loads relevant compliance rules from Qdrant (vector database).
#    - It validates the submitted IaC content against those rules using the validation engine.
#    - Publishes the result as an event (RabbitMQ) so the dashboard can update in real-time.
#
#  ENDPOINTS:
#    - POST /validate-framework: Accepts IaC file and framework, returns validation report.
#
#  INTEGRATION:
#    - Called from the frontend or API gateway after a user uploads a framework or IaC doc.
#    - Sends status/events to the dashboard via the "validation.pipeline" queue (RabbitMQ).
#
#  HOW TO EXTEND:
#    - Improve rule loading logic in qdrant_utils.py if supporting more frameworks.
#    - Adjust validate_iac_against_rules for additional IaC formats.
#    - Add new events or outputs as needed for more detailed dashboarding.
# =============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from qdrant_utils import get_rules_from_qdrant       # Loads compliance rules for framework
from validation_utils import validate_iac_against_rules   # Validates IaC against rules
from event_bus import publish_event                  # Publishes event for dashboard

UPLOAD_DIR = "uploads"
import os; os.makedirs(UPLOAD_DIR, exist_ok=True)    # Ensure upload folder exists

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin frontend access

# -----------------------------------------------------------------------
# POST /validate-framework
# Receives an IaC file and framework name; validates config against rules
# -----------------------------------------------------------------------
@app.route('/validate-framework', methods=['POST'])
def validate_framework():
    # --- Step 1: Receive IaC (YAML/Terraform) and framework ---
    iac_file = request.files["iac"]
    iac_content = iac_file.read().decode("utf-8")
    framework = request.form["framework"]

    # --- Step 2: Load rules from Qdrant (vector DB) ---
    rules = get_rules_from_qdrant(framework)

    # --- Step 3: Validate IaC against compliance rules ---
    validation_result = validate_iac_against_rules(iac_content, rules)

    # --- Step 4: Publish validation event to RabbitMQ for live dashboard updates ---
    event_payload = {
        "status": "done",
        "pipeline": "framework-validator",
        "framework": framework,
        "validation_result": validation_result
    }
    publish_event("validation.pipeline", event_payload)

    # --- Step 5: Return validation result to client (UI/API Gateway) ---
    return jsonify(validation_result)

# -----------------------------------------------------------------------
# Entry point: runs the Flask server on port 5020 in debug mode.
# -----------------------------------------------------------------------
if __name__ == "__main__":
    # CRITICAL FIX: bind to host="0.0.0.0" so Docker port mapping works!
    app.run(host="0.0.0.0", port=5020, debug=True)

# =============================================================================
#  End of app.py (Cloud Compliance Framework Validator)
# =============================================================================
