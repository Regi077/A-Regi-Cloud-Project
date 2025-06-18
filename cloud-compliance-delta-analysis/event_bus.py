# =============================================================================
#  event_bus.py  --  RabbitMQ Event Publisher for Delta Analysis Microservice
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - This utility module provides simple functions to publish events
#      (as JSON) to RabbitMQ, so other services or dashboards can react
#      in real time to pipeline state changes.
#    - Used for real-time updates in the overall compliance platform.
#
#  HOW IT WORKS:
#    - get_connection() establishes a connection to RabbitMQ using the
#      universal credentials (admin/password, as configured in docker-compose).
#    - publish_event(topic, payload) sends a durable message to the
#      specified queue/topic, with the payload serialized as JSON.
#    - Always closes the connection after publishing to avoid resource leaks.
# =============================================================================

import pika
import json

def get_connection():
    """
    Establish a connection to the RabbitMQ broker using hardcoded credentials.
    Note: If credentials change in docker-compose, update here as well.
    """
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',  # The Docker Compose service name (not 'localhost' in container)
            credentials=pika.PlainCredentials('admin', 'password')
        )
    )

def publish_event(topic, payload):
    """
    Publishes a JSON event to the specified RabbitMQ queue.
    The event is marked as durable (won’t be lost if RabbitMQ restarts).
    Args:
        topic (str): The event queue/topic name, e.g., "delta.pipeline"
        payload (dict): The event data to be sent (will be JSON-encoded)
    """
    connection = get_connection()
    channel = connection.channel()
    # Ensure the queue exists and is durable (survives restarts)
    channel.queue_declare(queue=topic, durable=True)
    channel.basic_publish(
        exchange='',  # Default exchange (direct to queue)
        routing_key=topic,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )
    connection.close()

# =============================================================================
#  End of event_bus.py  (Publishes events for dashboard and orchestration)
# =============================================================================
