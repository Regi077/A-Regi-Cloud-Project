# =============================================================================
#  event_bus.py  --  RabbitMQ Event Publishing for Framework Validator Pipeline
# =============================================================================
#  Author: Reginald / Team
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Provides lightweight functions for publishing events/messages to RabbitMQ.
#    - Used for real-time communication between microservices and dashboard.
#
#  USAGE:
#    - Call publish_event(topic, payload) from anywhere in the pipeline to emit a message.
#    - Ensures every event is delivered reliably (durable queues).
#    - Uses environment variables for robust Docker, cloud, and on-prem support.
#
#  CONFIGURATION (via environment or Docker Compose):
#    - RABBITMQ_HOST: default "rabbitmq"
#    - RABBITMQ_PORT: default 5672
#    - RABBITMQ_USER: default "admin"
#    - RABBITMQ_PASS: default "password"
# =============================================================================

import pika
import os
import json

def get_connection():
    """
    Establish a connection to the RabbitMQ broker using robust environment-based config.
    All values are overridable via env vars for seamless dev, prod, and Azure deployments.
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
    Publish a JSON-serializable event (payload) to a specified topic (queue).
    Durable queue ensures events survive RabbitMQ restarts.
    Closes connection after publish for safety (stateless pattern).
    """
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=topic, durable=True)  # Safe: will create if not exist
    channel.basic_publish(
        exchange='',
        routing_key=topic,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent messages
    )
    connection.close()

# =============================================================================
#  End of event_bus.py (simple, robust RabbitMQ publish utility)
# =============================================================================
