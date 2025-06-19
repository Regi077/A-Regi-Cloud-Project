# =============================================================================
#  app.py  --  Cloud Compliance Delta Analysis Service
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Provides API endpoints to compare pre- and post-remediation JSONs and
#      generate difference (delta) reports for compliance.
#    - Publishes delta-analysis results to RabbitMQ for live dashboard/UI updates.
#    - Supports PDF export of delta report (for download or audit evidence).
#
#  MAIN ENDPOINTS:
#    - POST /compare : Accepts two JSON objects ('pre', 'post') and returns the
#                      computed delta (difference table + summary).
#    - POST /export  : Accepts a 'delta' JSON (from /compare), generates a PDF,
#                      and returns it as a downloadable file.
#
#  INTERNALS:
#    - Uses delta_utils.compare_jsons() for field-level diff logic.
#    - Reports saved to the /reports folder (mounted as a Docker volume).
#    - Publishes every /compare result to the 'delta.pipeline' RabbitMQ topic.
# =============================================================================

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from delta_utils import compare_jsons        # Your custom diff logic module
import os

from event_bus import publish_event          # For RabbitMQ event streaming

app = Flask(__name__)
CORS(app)
os.makedirs("reports", exist_ok=True)        # Ensure report directory exists

# --------------------------------------------------------
# Endpoint: POST /compare
# Description: Calculate and return the delta (diff) between
# pre- and post-remediation JSON system states.
# --------------------------------------------------------
@app.route("/compare", methods=["POST"])
def compare():
    # Parse JSON input with keys 'pre' and 'post'
    data = request.json
    pre = data.get("pre")
    post = data.get("post")
    result = compare_jsons(pre, post)            # Compute delta (diff/summary)

    # Publish pipeline event to RabbitMQ for dashboard/UI
    event_payload = {
        "status": "done",
        "pipeline": "delta-analysis",
        "delta_result": result
    }
    publish_event("delta.pipeline", event_payload)

    return jsonify(result)                       # Return diff as JSON

# --------------------------------------------------------
# Endpoint: POST /export
# Description: Accept a delta result (from /compare) and
# generate a downloadable PDF compliance report.
# --------------------------------------------------------
@app.route("/export", methods=["POST"])
def export():
    # Generate PDF report with ReportLab
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    result = request.json.get("delta")
    filename = os.path.join("reports", "delta_report.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(30, 750, "Cloud Compliance Delta Report")
    y = 730
    for change in result["changes"]:
        c.drawString(30, y, f"{change['field']}: {change['before']} -> {change['after']}")
        y -= 15
    c.save()
    # Serve the file as a download
    return send_file(filename, as_attachment=True)

# --------------------------------------------------------
# App entrypoint: Runs Flask on port 5050 in debug mode.
# (Use production-ready server in prod.)
# --------------------------------------------------------
if __name__ == "__main__":
    # IMPORTANT: Bind to 0.0.0.0 so Docker Compose port mapping works!
    app.run(host="0.0.0.0", port=5050, debug=True)

# =============================================================================
#  End of app.py (Delta Analysis microservice)
# =============================================================================
