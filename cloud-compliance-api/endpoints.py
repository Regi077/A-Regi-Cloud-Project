
# Only admin and Service Provider can upload documents, start scans, and submit logs
# All roles can get frameworks (for viewing).

from flask import Blueprint, request, jsonify
from auth import require_auth
from rbac import require_role
from audit import audit_log

api = Blueprint("api", __name__)

@api.route("/upload-doc", methods=["POST"])
@require_auth
@require_role("admin", "Service Provider")
def upload_doc():
    user = request.user
    data = request.get_json()
    audit_log("upload-doc", user, {"filename": data.get("filename")})
    return jsonify({"message": "Document uploaded (dummy)", "filename": data.get("filename")})

@api.route("/get-frameworks", methods=["GET"])
@require_auth
def get_frameworks():
    user = request.user
    audit_log("get-frameworks", user)
    return jsonify({"frameworks": ["NIST 800-53", "PCI-DSS", "GDPR"]})

@api.route("/start-scan", methods=["POST"])
@require_auth
@require_role("admin", "Service Provider")
def start_scan():
    user = request.user
    data = request.get_json()
    audit_log("start-scan", user, {"target": data.get("target")})
    return jsonify({"message": "Scan started (dummy)", "target": data.get("target")})

@api.route("/submit-logs", methods=["POST"])
@require_auth
@require_role("admin", "Service Provider")
def submit_logs():
    user = request.user
    data = request.get_json()
    audit_log("submit-logs", user, {"content": data.get("logs")})
    return jsonify({"message": "Logs submitted (dummy)", "received": True})

