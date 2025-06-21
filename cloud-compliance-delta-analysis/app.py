# =============================================================================
#  app.py  --  Cloud Compliance Delta Analysis Service
# =============================================================================
#  Author: Reginald
#  Last updated: 21st June 2025
#
#  DESCRIPTION:
#    - Provides API endpoints to compare pre- and post-remediation JSONs and
#      generate difference (delta) reports for compliance verification.
#    - Publishes delta-analysis results to RabbitMQ for real-time dashboard and UI updates.
#    - Supports PDF export of delta reports for download or audit evidence.
#
#  MAIN ENDPOINTS:
#    - GET  /        : Health check endpoint to confirm service availability.
#    - POST /compare : Accepts two JSON objects ('pre' and 'post') representing
#                      system states, returns the computed delta including detailed
#                      field-level differences and summary.
#    - POST /export  : Accepts a delta JSON (result from /compare), generates a PDF
#                      report, and serves it as a downloadable file.
#
#  INTERNALS:
#    - Uses delta_utils.compare_jsons() for precise field-level diffing.
#    - Stores generated PDF reports in the /reports folder (Docker volume mounted).
#    - Publishes every /compare result as an event on the 'delta.pipeline' RabbitMQ topic.
# =============================================================================

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from delta_utils import compare_jsons        # Custom diff computation logic
import os

from event_bus import publish_event          # For publishing to RabbitMQ

# -----------------------------------------------------------------------------
# Initialize Flask app and enable CORS for frontend integration
# Ensure that the "reports" directory exists to store generated PDF files
# -----------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)
os.makedirs("reports", exist_ok=True)

# -----------------------------------------------------------------------------
# Favicon handler for browser requests (prevents 404 log spam)
# -----------------------------------------------------------------------------
@app.route('/favicon.ico')
def favicon():
    """
    Serves favicon.ico from static directory for browser requests.
    Prevents repetitive 404s in logs and browser devtools.
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
    Confirms that the delta-analysis service is running and reachable.
    Prevents 404 errors when accessing the base URL.
    """
    return "Delta Analysis service is running", 200

@app.route("/compare", methods=["POST"])
def compare():
    """
    POST /compare endpoint:
    - Accepts JSON payload with 'pre' and 'post' keys representing system states.
    - Computes the delta report highlighting changes between pre- and post-remediation.
    - Publishes the delta result to RabbitMQ for live dashboard updates.
    - Returns the delta report as a JSON response.
    """
    data = request.json
    pre = data.get("pre")
    post = data.get("post")

    # Compute field-level delta between the two JSON objects
    result = compare_jsons(pre, post)

    # Prepare event payload to broadcast the result on RabbitMQ topic
    event_payload = {
        "status": "done",
        "pipeline": "delta-analysis",
        "delta_result": result
    }
    publish_event("delta.pipeline", event_payload)

    # Return delta analysis result to the API caller
    return jsonify(result)

@app.route("/export", methods=["POST"])
def export():
    """
    POST /export endpoint:
    - Accepts a delta JSON payload (from /compare).
    - Generates a PDF report summarizing the delta changes.
    - Saves the report to the /reports directory.
    - Serves the PDF as a downloadable file.
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    result = request.json.get("delta")
    filename = os.path.join("reports", "delta_report.pdf")

    # Create PDF canvas and add header/title
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(30, 750, "Cloud Compliance Delta Report")

    # Write each delta change line by line with proper spacing
    y = 730
    for change in result["changes"]:
        c.drawString(30, y, f"{change['field']}: {change['before']} -> {change['after']}")
        y -= 15

    # Save the PDF file
    c.save()

    # Return the generated PDF as a downloadable file to the client
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    """
    Main entrypoint for the Flask microservice.
    Runs the server on port 5050, binding to all interfaces (0.0.0.0)
    to support Docker container port forwarding.
    Debug mode enabled for development purposes only.
    """
    app.run(host="0.0.0.0", port=5050, debug=True)

# =============================================================================
#  End of app.py (Delta Analysis microservice)
# =============================================================================
