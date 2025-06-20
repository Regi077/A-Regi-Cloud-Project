# =============================================================================
#  app.py  --  IaC Analysis & Remediation Microservice (Cloud Compliance Tool)
# =============================================================================
#  Author: Reginald
#  Last updated: 20th June 2025
#
#  DESCRIPTION:
#    - Flask microservice for analyzing Infrastructure as Code (IaC) files
#      (YAML, Terraform, etc.) against compliance frameworks.
#    - Suggests auto-remediation blocks based on analysis results.
#    - Publishes live events to RabbitMQ for real-time dashboard updates.
#
#  USAGE:
#    - GET /             : Health check endpoint confirming service is running.
#    - POST /analyze-iac : Accepts IaC file and framework name.
#    - Returns: JSON with pass/fail status and remediation suggestions.
#    - All uploads are saved to an "uploads" folder.
#
#  PIPELINE INTEGRATION:
#    - Publishes "remediation.pipeline" events for live UI feedback.
# =============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from remediation_engine import analyze_and_remediate        # Core analysis logic
from event_bus import publish_event                          # Event publishing to RabbitMQ

import os

# -----------------------------------------------------------------------------
# Create upload directory if not exists
# Ensures all incoming IaC files have a storage location
# -----------------------------------------------------------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# Initialize Flask application instance
# Enable CORS to allow cross-origin frontend access for API calls
# -----------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    """
    Root health check endpoint.
    Confirms service availability and prevents 404 on root path access.
    Used by health checks or simple connectivity tests.
    """
    return "IaC Analysis service is running", 200

@app.route('/analyze-iac', methods=['POST'])
def analyze_iac():
    """
    POST /analyze-iac endpoint:
    - Accepts an Infrastructure-as-Code file ('iac') and a compliance framework name.
    - Reads and decodes IaC file content.
    - Runs analysis and remediation logic against the given framework.
    - Publishes analysis result events to RabbitMQ for real-time UI updates.
    - Returns a JSON payload with pass/fail status and remediation recommendations.

    Handles exceptions gracefully by returning a 500 error with message.
    """
    try:
        # Extract uploaded file and framework name from request
        iac_file = request.files["iac"]
        framework = request.form["framework"]
        iac_content = iac_file.read().decode("utf-8")   # Decode file bytes to string

        # Analyze IaC content for compliance and generate remediation suggestions
        analysis = analyze_and_remediate(iac_content, framework)

        # Prepare event payload for observability and dashboard updates
        event_payload = {
            "status": "done",
            "pipeline": "iac-analysis",
            "framework": framework,
            "analysis_result": analysis
        }
        # Publish event to RabbitMQ event bus
        publish_event("remediation.pipeline", event_payload)

        # Return the analysis result to the client as JSON
        return jsonify(analysis)

    except Exception as e:
        # Capture unexpected errors and respond with error details
        return jsonify({"status": "error", "message": str(e)}), 500

@app.errorhandler(405)
def method_not_allowed(e):
    """
    Handler for HTTP 405 Method Not Allowed errors.
    Returns a JSON response describing the error.
    Ensures API clients receive clear feedback on unsupported HTTP methods.
    """
    return jsonify({"error": "Method not allowed", "message": str(e)}), 405

# -----------------------------------------------------------------------------
# Application Entrypoint
# Runs the Flask development server on all network interfaces (0.0.0.0)
# Port 5030 is used for the IaC Analysis microservice.
# Debug mode is enabled for development only and should be disabled in production.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5030, debug=True)

# =============================================================================
#  End of app.py (cloud-compliance-iac-analysis)
# =============================================================================
