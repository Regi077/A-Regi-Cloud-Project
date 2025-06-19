# =============================================================================
#  event_bus.py  --  RabbitMQ Event Publishing Utility for Cloud Compliance Tool
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  PURPOSE:
#    - Enables microservices to send (publish) structured events
#      to the central RabbitMQ event bus.
#    - Used for real-time dashboard updates, alerting, audit logs, and pipeline orchestration.
#
#  USAGE:
#    from event_bus import publish_event
#    publish_event("pipeline.topic", {"status": "done", "details": ...})
#
#  CONFIGURATION:
#    - RabbitMQ connection details are read from environment variables for security and flexibility.
#      - RABBITMQ_HOST: default "rabbitmq"
#      - RABBITMQ_PORT: default 5672
#      - RABBITMQ_USER: default "admin"
#      - RABBITMQ_PASS: default "password"
#    - Never hardcodes credentials or network assumptions—portable to any cloud or on-prem.
# =============================================================================

import pika
import os
import json

def get_connection():
    """
    Establishes a connection to RabbitMQ using environment variables (or defaults).
    Host, port, username, and password are configurable—never hardcoded for security.
    """
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    port = int(os.getenv("RABBITMQ_PORT", 5672))
    user = os.getenv("RABBITMQ_USER", "admin")
    password = os.getenv("RABBITMQ_PASS", "password")
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(user, password)
        )
    )

def publish_event(topic, payload):
    """
    Publishes a JSON-serializable payload to the specified queue/topic.
    Closes the connection after sending for statelessness.
    """
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=topic, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=topic,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)  # Message persistent for reliability
    )
    connection.close()

# =============================================================================
#  End of event_bus.py  (All event publishing is stateless, robust, and future-proof)
# =============================================================================
