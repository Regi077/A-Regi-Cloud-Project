# =============================================================================
#  app.py  --  IaC Analysis & Remediation Microservice (Cloud Compliance Tool)
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Flask microservice for analyzing Infrastructure as Code (IaC) files
#      (YAML, Terraform, etc.) against compliance frameworks.
#    - Suggests auto-remediation blocks based on analysis results.
#    - Publishes live events to RabbitMQ for real-time dashboard updates.
#
#  USAGE:
#    - POST /analyze-iac (multipart/form-data: 'iac' file, 'framework' name)
#    - Returns: JSON with pass/fail status and remediation suggestions.
#    - All uploads are saved to an "uploads" folder.
#
#  PIPELINE INTEGRATION:
#    - Publishes "remediation.pipeline" events for live UI feedback.
# =============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from remediation_engine import analyze_and_remediate        # Core analysis logic
from event_bus import publish_event                        # Event publishing to RabbitMQ

# --- Set up upload directory for incoming IaC files ---
UPLOAD_DIR = "uploads"
import os; os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Flask app initialization ---
app = Flask(__name__)
CORS(app)    # Enable CORS for cross-origin frontend requests

# --------------------------------------------------------------------------
# Analyze IaC Endpoint
# POST /analyze-iac
# Accepts: IaC file (as 'iac'), framework name (as 'framework' in form-data)
# Returns: JSON report of analysis & remediation suggestions
# --------------------------------------------------------------------------
@app.route('/analyze-iac', methods=['POST'])
def analyze_iac():
    # --- File & framework extraction ---
    iac_file = request.files["iac"]
    framework = request.form["framework"]
    iac_content = iac_file.read().decode("utf-8")   # Convert to string

    # --- Analyze IaC against compliance rules ---
    analysis = analyze_and_remediate(iac_content, framework)

    # --- Publish live update to RabbitMQ for dashboard/observability ---
    event_payload = {
        "status": "done",
        "pipeline": "iac-analysis",
        "framework": framework,
        "analysis_result": analysis
    }
    publish_event("remediation.pipeline", event_payload)

    # --- Return analysis result as JSON ---
    return jsonify(analysis)

# --------------------------------------------------------------------------
# Start the Flask microservice (runs on port 5030)
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # CRITICAL: Bind to all interfaces for Docker container compatibility
    app.run(host="0.0.0.0", port=5030, debug=True)

# =============================================================================
#  End of app.py (cloud-compliance-iac-analysis)
# =============================================================================
