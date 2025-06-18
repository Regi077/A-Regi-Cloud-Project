# =============================================================================
# cloud-compliance-dashboard/app.py
#
# Author: Reginald
# Last updated: 18th June 2025
#
# Description:
#   Dashboard backend for the Cloud Compliance Tool.
#   - Uses Flask and Flask-SocketIO to relay real-time pipeline events to the UI.
#   - Consumes events (via RabbitMQ) from all major backend pipelines, emitting
#     them as WebSocket broadcasts to any connected React UI clients.
#   - Each event topic (pipeline) runs on its own background thread for scalability.
#
# Usage:
#   - Start via Docker Compose, or directly with: python app.py
#   - Accessible at http://localhost:5001 (or mapped port).
#
# Environment:
#   - Requires RabbitMQ (as per docker-compose) and compatible event bus settings.
# =============================================================================

from flask import Flask
from flask_socketio import SocketIO
import threading
from event_bus import consume_events  # Custom util for subscribing to RabbitMQ events

# --- Initialize Flask app and SocketIO for real-time WebSocket comms ---
app = Flask(__name__)
# Allow cross-origin SocketIO connections from the UI (localhost:3000)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Emit incoming event to all connected dashboard clients ---
def dashboard_event_handler(event):
    """
    Called for every event consumed from RabbitMQ.
    Broadcasts the event to all active WebSocket clients under 'pipeline_update'.
    """
    socketio.emit('pipeline_update', event)

# --- Each topic runs in a separate thread to keep event flow non-blocking ---
def listen_to_topic(topic):
    """
    Persistent background consumer for a given RabbitMQ topic.
    Calls dashboard_event_handler for every received event.
    """
    while True:
        consume_events(topic, dashboard_event_handler)

# --- Simple HTTP health check route for diagnostics ---
@app.route('/')
def home():
    return "Dashboard backend running!"

if __name__ == '__main__':
    # Topics (RabbitMQ queues) to subscribe to; keep in sync with your microservices
    topics = [
        "rule.ingestion",
        "validation.pipeline",
        "remediation.pipeline",
        "iam.pipeline",
        "delta.pipeline"
    ]
    # Start a thread for each topic to ensure parallel event handling
    for topic in topics:
        thread = threading.Thread(target=listen_to_topic, args=(topic,), daemon=True)
        thread.start()

    # Start the SocketIO server (Flask dev server not for production)
    socketio.run(app, host='0.0.0.0', port=5000)
