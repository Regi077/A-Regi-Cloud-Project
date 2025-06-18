# This code sets up a Flask application with SocketIO to handle real-time updates
# from various event topics. It listens to specified topics and emits updates
# to connected clients via WebSocket. Each topic is handled in a separate thread
# to ensure the application remains responsive.

from flask import Flask
from flask_socketio import SocketIO
import threading
from event_bus import consume_events

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Handler to emit events to all dashboard clients
def dashboard_event_handler(event):
    socketio.emit('pipeline_update', event)

# Background thread for each topic
def listen_to_topic(topic):
    while True:
        consume_events(topic, dashboard_event_handler)

@app.route('/')
def home():
    return "Dashboard backend running!"

if __name__ == '__main__':
    # List all topics you want to listen to
    topics = [
        "rule.ingestion",
        "validation.pipeline",
        "remediation.pipeline",
        "iam.pipeline",
        "delta.pipeline"
    ]
    for topic in topics:
        thread = threading.Thread(target=listen_to_topic, args=(topic,), daemon=True)
        thread.start()

    socketio.run(app, host='0.0.0.0', port=5000)

