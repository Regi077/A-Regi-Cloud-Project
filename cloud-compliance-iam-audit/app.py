# This is the main entry point for the Flask application.
# It sets up the Flask app, enables CORS, and defines the endpoint for IAM auditing.
# The endpoint accepts JSON data, processes it using the `audit_iam` function,
# and returns the result as a JSON response.

from flask import Flask, request, jsonify
from flask_cors import CORS
from iam_audit_engine import audit_iam

from event_bus import publish_event  # <-- NEW

UPLOAD_DIR = "uploads"
import os; os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.route('/audit-iam', methods=['POST'])
def audit_iam_endpoint():
    data = request.get_json()
    result = audit_iam(data)

    # Publish event to RabbitMQ for dashboard/UI update  <-- NEW
    event_payload = {
        "status": "done",
        "pipeline": "iam-audit",
        "audit_result": result
    }
    publish_event("iam.pipeline", event_payload)

    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5040, debug=True)
# This code sets up a Flask application that listens for POST requests on the /audit-iam endpoint.
# When a request is received, it processes the JSON data using the `audit_iam` function