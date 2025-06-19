# =============================================================================
#  Cloud Compliance API Gateway (app.py)
# =============================================================================
#  This is the main Flask application entry point for the Cloud Compliance API.
#  - Handles API routing, rate-limiting, and CORS for secure microservice access.
#  - Publishes audit and observability events (user login/logout, API calls, errors)
#    to the event bus (RabbitMQ) for live monitoring and compliance logs.
#  - Integrates with all core endpoints via a Flask blueprint (see endpoints.py).
#
#  Best Practices:
#    - Run in debug=True for local/dev, but always use debug=False in production.
#    - In production, use a robust WSGI server (e.g., Gunicorn, uWSGI) behind a reverse proxy.
#    - All sensitive/secret config (API keys, DB URIs) should be managed with env vars or secrets, not hardcoded.
#
#  Author: Reginald
#  Last updated: 18th June 2025
# =============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from endpoints import api   # Custom blueprint for business logic endpoints

from event_bus import publish_event
import datetime

# -----------------------------------------------------------------------------
# App Initialization
# -----------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for UI/frontend calls

# -----------------------------------------------------------------------------
# Rate Limiting (Prevent brute force/API abuse)
# -----------------------------------------------------------------------------
limiter = Limiter(
    key_func=get_remote_address,         # Identify clients by IP address
    default_limits=["30/minute"]         # 30 API calls per minute per client
)
limiter.init_app(app)

# -----------------------------------------------------------------------------
# Register All Application Endpoints
# -----------------------------------------------------------------------------
app.register_blueprint(api)  # All business logic endpoints in endpoints.py

# -----------------------------------------------------------------------------
# Helper: Structured Audit/Event Publisher
# -----------------------------------------------------------------------------
def audit_event(topic, action, user=None, extra=None):
    """
    Publishes a structured audit/compliance event to RabbitMQ.
    All major actions (user login/logout, API errors, key requests) are tracked.
    """
    payload = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "action": action,
        "user": user,
        "extra": extra or {}
    }
    publish_event(topic, payload)

# -----------------------------------------------------------------------------
# API Endpoints: User Session (Login/Logout)
# -----------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint for user authentication.
    Emits a 'user.activity' event for audit trail.
    """
    data = request.get_json()
    username = data.get("username")
    # TODO: Insert your actual user authentication logic here!
    audit_event("user.activity", "login", user=username)
    return jsonify({"success": True})

@app.route('/logout', methods=['POST'])
def logout():
    """
    Logout endpoint for user session termination.
    Emits a 'user.activity' event for audit trail.
    """
    data = request.get_json()
    username = data.get("username")
    # TODO: Insert your actual logout/session invalidation logic here!
    audit_event("user.activity", "logout", user=username)
    return jsonify({"success": True})

# -----------------------------------------------------------------------------
# API Endpoint: Health Check
# -----------------------------------------------------------------------------
@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint for liveness/readiness probes.
    Emits a 'system.health' event for operational monitoring.
    """
    audit_event("system.health", "api_health_check", extra={"status": "OK"})
    return jsonify({"status": "OK"})

# -----------------------------------------------------------------------------
# Global Error Handler: Observability & Security Alerts
# -----------------------------------------------------------------------------
@app.errorhandler(Exception)
def handle_error(e):
    """
    Catches unhandled exceptions and logs an alert event.
    Ensures that errors are both auditable and visible in observability tooling.
    """
    audit_event(
        "security.alert",
        "error",
        user=request.json.get("username") if request.is_json and request.json else None,
        extra={"error": str(e), "endpoint": request.path}
    )
    return jsonify({"error": str(e)}), 500

# -----------------------------------------------------------------------------
# Selective API Access Auditing: Regulatory Logging (Only for Key Endpoints)
# -----------------------------------------------------------------------------
AUDIT_ENDPOINTS = {
    "/login",
    "/logout",
    "/upload-doc",
    "/submit-logs",
    "/start-scan",
    "/submit-remediation",
    "/audit-iam"
}

@app.before_request
def log_selected_api_access():
    """
    Logs API access events only for selected sensitive endpoints.
    These logs are critical for regulatory compliance and incident response.
    """
    if request.path in AUDIT_ENDPOINTS:
        audit_event(
            "audit.log",
            "api_access",
            user=(request.json.get("username") if request.is_json and request.json else None),
            extra={"method": request.method, "path": request.path}
        )

# -----------------------------------------------------------------------------
# Main Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # NOTE: host='0.0.0.0' required for Docker port mapping
    app.run(host="0.0.0.0", port=5000, debug=True)  # In production: use debug=False and WSGI server

# =============================================================================
#  End of app.py
# =============================================================================
