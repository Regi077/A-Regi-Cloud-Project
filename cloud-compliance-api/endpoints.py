# =============================================================================
#  endpoints.py  --  Cloud Compliance API Endpoints (Role-Based Access Control)
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Defines API endpoints for document upload, framework listing, scan initiation, and log submission.
#    - Implements RBAC so only Admin/Service Provider can upload, scan, or submit logs.
#    - All roles can list/view frameworks.
#
#  KEY MIDDLEWARES:
#    - @require_auth: Checks if user is authenticated (auth.py).
#    - @require_role: Checks if user's role matches the endpoint's required roles (rbac.py).
#    - audit_log: Records every critical API action for traceability (audit.py).
#
#  HOW TO EXTEND:
#    - Add new endpoints as needed. Decorate with RBAC/auth as required.
#    - Only adjust role restrictions if new use cases demand it.
# =============================================================================

from flask import Blueprint, request, jsonify
from auth import require_auth             # Authentication: user must be logged in
from rbac import require_role             # Authorization: user must have right role
from audit import audit_log               # For compliance/audit trail logging

api = Blueprint("api", __name__)          # Flask Blueprint for clean API registration

# ------------------------------------------------------------
# Upload Compliance Document (RBAC: Admin, Service Provider)
# ------------------------------------------------------------
@api.route("/upload-doc", methods=["POST"])
@require_auth
@require_role("admin", "Service Provider")
def upload_doc():
    """
    Allows Admin/Service Provider to upload a compliance document.
    Records the action in the audit log.
    """
    user = request.user
    data = request.get_json()
    audit_log("upload-doc", user, {"filename": data.get("filename")})
    return jsonify({
        "message": "Document uploaded (dummy)",  # Stubbed, replace with real logic later
        "filename": data.get("filename")
    })

# ------------------------------------------------------------
# List Compliance Frameworks (RBAC: All Authenticated Users)
# ------------------------------------------------------------
@api.route("/get-frameworks", methods=["GET"])
@require_auth
def get_frameworks():
    """
    Returns a list of available compliance frameworks.
    All logged-in users can access this endpoint.
    """
    user = request.user
    audit_log("get-frameworks", user)
    return jsonify({
        "frameworks": ["NIST 800-53", "PCI-DSS", "GDPR"]
    })

# ------------------------------------------------------------
# Start a Compliance Scan (RBAC: Admin, Service Provider)
# ------------------------------------------------------------
@api.route("/start-scan", methods=["POST"])
@require_auth
@require_role("admin", "Service Provider")
def start_scan():
    """
    Allows Admin/Service Provider to initiate a scan.
    Records action and parameters in the audit log.
    """
    user = request.user
    data = request.get_json()
    audit_log("start-scan", user, {"target": data.get("target")})
    return jsonify({
        "message": "Scan started (dummy)",
        "target": data.get("target")
    })

# ------------------------------------------------------------
# Submit System Logs (RBAC: Admin, Service Provider)
# ------------------------------------------------------------
@api.route("/submit-logs", methods=["POST"])
@require_auth
@require_role("admin", "Service Provider")
def submit_logs():
    """
    Allows Admin/Service Provider to submit log data.
    Logs the submission event for compliance auditing.
    """
    user = request.user
    data = request.get_json()
    audit_log("submit-logs", user, {"content": data.get("logs")})
    return jsonify({
        "message": "Logs submitted (dummy)",
        "received": True
    })

# =============================================================================
#  End of endpoints.py  (All endpoints RBAC-protected, audit-logged)
# =============================================================================
