# =============================================================================
#  app.py  --  IAM Role Audit Microservice (Cloud Compliance Pipeline)
# =============================================================================
#  Author: Reginald
#  Last updated: 21st June 2025
#
#  DESCRIPTION:
#    - Main entry point for the IAM audit microservice.
#    - Exposes a single POST /audit-iam endpoint for receiving IAM JSON data.
#    - Performs compliance audit on IAM roles, users, and policies.
#    - Returns a detailed risk-scored report as JSON.
#    - Publishes audit results to RabbitMQ for real-time dashboard updates.
#
#  KEY COMPONENTS:
#    - Flask: lightweight Python web framework.
#    - Flask-CORS: enables cross-origin requests from frontend UI.
#    - iam_audit_engine.py: custom logic to evaluate IAM compliance.
#    - event_bus.py: manages publishing events to RabbitMQ.
#
#  USAGE:
#    - POST IAM role/policy JSON data to /audit-iam.
#    - Receive risk analysis and audit details in response.
#    - Results automatically broadcast to live dashboard/UI.
# =============================================================================

from flask import Flask, request, jsonify, send_from_directory  # Add send_from_directory
from flask_cors import CORS
from iam_audit_engine import audit_iam        # Custom IAM audit logic
from event_bus import publish_event           # Event bus for observability

import os

# -----------------------------------------------------------------------------
# Create uploads directory for any file-based needs (future-proofing)
# -----------------------------------------------------------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# Initialize Flask app instance
# Enable CORS for cross-origin requests from UI frontends
# -----------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

# -----------------------------------------------------------------------------
# Serve favicon.ico from /static to prevent browser 404 noise
# -----------------------------------------------------------------------------
@app.route('/favicon.ico')
def favicon():
    """
    Serves favicon.ico from the static directory to eliminate 404s in browser tabs/logs.
    """
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/')
def root():
    """
    Root health check endpoint.
    Confirms the IAM audit service is live and reachable.
    Prevents 404 errors on accessing root URL.
    """
    return "IAM Audit service is running", 200

@app.route('/audit-iam', methods=['POST'])
def audit_iam_endpoint():
    """
    POST /audit-iam endpoint:
    - Accepts IAM JSON data (roles, users, policies) from request body.
    - Invokes custom audit logic to analyze compliance and risk.
    - Publishes audit results to RabbitMQ for real-time UI updates.
    - Returns risk-scored audit report as JSON.
    """
    # Parse JSON input payload
    data = request.get_json()

    # Perform IAM audit logic using imported engine
    result = audit_iam(data)

    # Structure event payload for observability dashboard
    event_payload = {
        "status": "done",
        "pipeline": "iam-audit",
        "audit_result": result
    }

    # Publish event asynchronously to RabbitMQ event bus
    publish_event("iam.pipeline", event_payload)

    # Return audit result to caller as JSON response
    return jsonify(result)

# -----------------------------------------------------------------------------
# Main entry point for running Flask development server.
# Binds to 0.0.0.0 for accessibility via Docker port mapping.
# Debug mode enabled for development; disable in production.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5040, debug=True)

# =============================================================================
#  End of app.py (IAM Audit Pipeline, event-driven and real-time dashboard-ready)
# =============================================================================
