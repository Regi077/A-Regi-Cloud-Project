# =============================================================================
#  event_bus.py  --  RabbitMQ Event Publishing Utility for Cloud Compliance Tool
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  PURPOSE:
#    - This utility enables microservices to send (publish) structured events
#      to the central RabbitMQ event bus.
#    - Used for real-time dashboard updates, alerting, audit logs, and pipeline orchestration.
#
#  USAGE:
#    from event_bus import publish_event
#    publish_event("pipeline.topic", {"status": "done", "details": ...})
#
#  CONFIGURATION:
#    - Assumes RabbitMQ is available at host 'rabbitmq' (Docker service name)
#    - Credentials must match those in docker-compose.yml (admin/password)
# =============================================================================

import pika
import json

def get_connection():
    """
    Create and return a new connection to RabbitMQ using hardcoded credentials.
    Assumes 'rabbitmq' is the Docker network hostname.
    """
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('admin', 'password')
        )
    )

def publish_event(topic, payload):
    """
    Publish a JSON-serializable payload to the specified queue/topic.
    - topic: str, the RabbitMQ queue name (e.g., "rule.ingestion")
    - payload: dict, the event/message to send
    Closes the connection after sending (stateless pattern).
    """
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=topic, durable=True)  # Ensure queue exists and is durable
    channel.basic_publish(
        exchange='',
        routing_key=topic,
        body=json.dumps(payload),                     # Serialize payload to JSON
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )
    connection.close()

# =============================================================================
#  End of event_bus.py  (All event publishing is stateless, reliable, and simple)
# =============================================================================
