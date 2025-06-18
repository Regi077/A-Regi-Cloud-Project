# =============================================================================
#  event_bus.py  --  Event Publishing Utilities for RabbitMQ for Cloud Compliance Rule Ingestion
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  PURPOSE:
#    - Provides functions for publishing events to RabbitMQ so that
#      other microservices and the dashboard can react to pipeline progress.
#
#  HOW IT WORKS:
#    - get_connection(): Creates a connection to the RabbitMQ broker using the
#      specified host and credentials (default: admin/password).
#    - publish_event(): Publishes a JSON-serializable payload to a named queue
#      (topic), with durability (message will survive broker restarts).
#
#  USAGE:
#    - Import and call publish_event("queue_name", {...}) from your pipeline code
# =============================================================================

import pika
import json

def get_connection():
    """
    Establishes a blocking connection to the RabbitMQ service.
    Uses 'admin' user and 'password' as set in docker-compose.yml.
    """
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',  # Must match the service name in Docker Compose
            credentials=pika.PlainCredentials('admin', 'password')
        )
    )

def publish_event(topic, payload):
    """
    Publishes an event to the specified RabbitMQ queue.

    Args:
        topic (str): The queue/topic to send to (e.g., 'rule.ingestion')
        payload (dict): A JSON-serializable dictionary (event data)

    Behavior:
        - Connects to RabbitMQ
        - Declares the queue durable (persists messages if broker restarts)
        - Sends the payload as a JSON string
        - Closes the connection
    """
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=topic, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=topic,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
    )
    connection.close()

# =============================================================================
#  End of event_bus.py (RabbitMQ event utility functions)
# =============================================================================
