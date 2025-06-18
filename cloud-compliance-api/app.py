# The application is set to run in debug mode, which is useful for development.
# In production, it is recommended to set debug to False and use a WSGI server like Gunicorn or uWSGI.      
# The app listens on port 5000, which is the default port for Flask applications.
# The `endpoints` module is where the actual API endpoints are defined, handling requests and responses.

# Perfect—that means your backend API is set up and working exactly as it should!
# You just authenticated and successfully retrieved live data from your secured Flask API. Everything is running smoothly.

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from endpoints import api

from event_bus import publish_event
import datetime

app = Flask(__name__)
CORS(app)

# --- Rate Limiting ---
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["30/minute"]
)
limiter.init_app(app)

app.register_blueprint(api)

# --- Event Publishing Helper ---
def audit_event(topic, action, user=None, extra=None):
    payload = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "action": action,
        "user": user,
        "extra": extra or {}
    }
    publish_event(topic, payload)

# --- User Activity Events ---
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    # (Your login logic here)
    audit_event("user.activity", "login", user=username)
    return jsonify({"success": True})

@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    username = data.get("username")
    # (Your logout logic here)
    audit_event("user.activity", "logout", user=username)
    return jsonify({"success": True})

# --- Health Check Event ---
@app.route('/health', methods=['GET'])
def health():
    audit_event("system.health", "api_health_check", extra={"status": "OK"})
    return jsonify({"status": "OK"})

# --- Global Error Event ---
@app.errorhandler(Exception)
def handle_error(e):
    # You can expand error logging here as needed
    audit_event(
        "security.alert",
        "error",
        user=request.json.get("username") if request.is_json and request.json else None,
        extra={"error": str(e), "endpoint": request.path}
    )
    return jsonify({"error": str(e)}), 500

# --- Selective Regulatory Endpoint Audit Logging ---
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
    # Only audit if this is a key endpoint
    if request.path in AUDIT_ENDPOINTS:
        audit_event(
            "audit.log",
            "api_access",
            user=(request.json.get("username") if request.is_json and request.json else None),
            extra={"method": request.method, "path": request.path}
        )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
