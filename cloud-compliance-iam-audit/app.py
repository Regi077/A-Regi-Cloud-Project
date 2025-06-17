# This is the main entry point for the Flask application.
# It sets up the Flask app, enables CORS, and defines the endpoint for IAM auditing.
# The endpoint accepts JSON data, processes it using the `audit_iam` function,
# and returns the result as a JSON response.

from flask import Flask, request, jsonify
from flask_cors import CORS
from iam_audit_engine import audit_iam

UPLOAD_DIR = "uploads"
import os; os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.route('/audit-iam', methods=['POST'])
def audit_iam_endpoint():
    data = request.get_json()
    result = audit_iam(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5040, debug=True)


