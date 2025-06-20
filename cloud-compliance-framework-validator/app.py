# =============================================================================
#  app.py  --  Cloud Compliance Framework Validator Microservice
# =============================================================================
#  Author: Reginald
#  Last updated: 20th June 2025
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

import os
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)    # Ensure upload folder exists

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin frontend access

@app.route('/')
def root():
    """
    Root route for health check.
    Returns a simple confirmation message to confirm the
    framework-validation service is alive and reachable.
    """
    return "Framework Validator service is running", 200

@app.route('/validate-framework', methods=['POST'])
def validate_framework():
    """
    POST /validate-framework
    Receives an IaC file and framework name; validates the IaC content
    against loaded compliance rules, publishes the results as events,
    and returns the validation report.
    """
    try:
        # Step 1: Receive IaC (YAML/Terraform) and framework
        iac_file = request.files["iac"]
        iac_content = iac_file.read().decode("utf-8")
        framework = request.form["framework"]

        # Step 2: Load compliance rules from Qdrant vector DB
        rules = get_rules_from_qdrant(framework)

        # Step 3: Validate IaC content against compliance rules
        validation_result = validate_iac_against_rules(iac_content, rules)

        # Step 4: Publish validation event to RabbitMQ for real-time dashboard update
        event_payload = {
            "status": "done",
            "pipeline": "framework-validator",
            "framework": framework,
            "validation_result": validation_result
        }
        publish_event("validation.pipeline", event_payload)

        # Step 5: Return validation results as JSON to client
        return jsonify(validation_result)

    except Exception as e:
        # Log error and return 500 with error details
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(405)
def method_not_allowed(e):
    """
    Handler for 405 Method Not Allowed errors.
    Returns a JSON response explaining allowed methods.
    """
    return jsonify({"error": "Method not allowed", "message": str(e)}), 405

if __name__ == "__main__":
    # CRITICAL FIX: bind to host="0.0.0.0" so Docker port mapping works!
    app.run(host="0.0.0.0", port=5020, debug=True)

# =============================================================================
#  End of app.py (Cloud Compliance Framework Validator)
# =============================================================================
