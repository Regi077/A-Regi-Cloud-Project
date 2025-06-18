from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from delta_utils import compare_jsons
import os

from event_bus import publish_event  

app = Flask(__name__)
CORS(app)
os.makedirs("reports", exist_ok=True)

@app.route("/compare", methods=["POST"])
def compare():
    data = request.json
    pre = data.get("pre")
    post = data.get("post")
    result = compare_jsons(pre, post)

    # Publish event to RabbitMQ for dashboard/UI update 
    event_payload = {
        "status": "done",
        "pipeline": "delta-analysis",
        "delta_result": result
    }
    publish_event("delta.pipeline", event_payload)

    return jsonify(result)

@app.route("/export", methods=["POST"])
def export():
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
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(port=5050, debug=True)
