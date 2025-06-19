# =============================================================================
#  app.py  --  IAM Role Audit Microservice (Cloud Compliance Pipeline)
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - This is the main entry point for the IAM audit pipeline.
#    - Sets up a Flask web application that exposes a single /audit-iam endpoint.
#    - Receives IAM JSON data, performs a compliance audit, and returns a risk-scored report.
#    - Publishes results to RabbitMQ so your real-time dashboard receives updates.
#
#  KEY COMPONENTS:
#    - Flask: lightweight Python web server.
#    - Flask-CORS: enables cross-origin requests from your UI.
#    - iam_audit_engine.py: custom logic for evaluating IAM roles, users, and policies.
#    - event_bus.py: handles event publishing for real-time observability.
#
#  USAGE:
#    - POST IAM role/policy JSON data to /audit-iam.
#    - Receives detailed risk results as JSON.
#    - Results automatically broadcast to dashboard and UI.
# =============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from iam_audit_engine import audit_iam
from event_bus import publish_event

UPLOAD_DIR = "uploads"
import os; os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains (for UI integration)

# -----------------------------------------------------------------------------
# Endpoint: /audit-iam
# Accepts: JSON payload with users, groups, and policies
# Returns: Risk analysis (high/medium/low) and audit issues
# -----------------------------------------------------------------------------
@app.route('/audit-iam', methods=['POST'])
def audit_iam_endpoint():
    data = request.get_json()
    result = audit_iam(data)

    # Publish this audit result to RabbitMQ for real-time dashboard update
    event_payload = {
        "status": "done",
        "pipeline": "iam-audit",
        "audit_result": result
    }
    publish_event("iam.pipeline", event_payload)

    return jsonify(result)

# -----------------------------------------------------------------------------
# Main Application Entry Point (Docker-ready: host="0.0.0.0")
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # IMPORTANT: Bind to 0.0.0.0 to be reachable via Docker port mapping
    app.run(host="0.0.0.0", port=5040, debug=True)

# =============================================================================
#  End of app.py (IAM Audit Pipeline, fully event-driven and dashboard-ready)
# =============================================================================
