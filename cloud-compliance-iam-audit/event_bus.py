# =============================================================================
#  event_bus.py  --  RabbitMQ Event Publisher Utility for IAM Audit Microservice
# =============================================================================
#  Author: Reginald 
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Provides utility functions for publishing pipeline events to RabbitMQ.
#    - Enables real-time status updates to the dashboard and orchestrates communication between microservices.
#
#  HOW IT WORKS:
#    - `get_connection()` establishes a new connection to RabbitMQ using the service's credentials.
#    - `publish_event(topic, payload)` serializes the payload to JSON and publishes it to the specified RabbitMQ queue.
#
#  USAGE:
#    - Call `publish_event("iam.pipeline", {...})` after processing requests to send updates downstream.
#    - Standardizes inter-service communication and real-time dashboard observability.
# =============================================================================

import pika
import json

def get_connection():
    """
    Establish a connection to the RabbitMQ broker running on the 'rabbitmq' service
    using the universal admin/password credentials.
    """
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',  # This matches your docker-compose service name
            credentials=pika.PlainCredentials('admin', 'password')
        )
    )

def publish_event(topic, payload):
    """
    Publishes a JSON-serialized payload to the specified RabbitMQ queue (topic).
    Marks messages as durable for reliability. Call this after each key operation.
    """
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=topic, durable=True)  # Durable queue for persistence
    channel.basic_publish(
        exchange='',
        routing_key=topic,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)  # Make messages persistent
    )
    connection.close()

# =============================================================================
#  End of event_bus.py (Plug-and-play RabbitMQ integration for pipeline events)
# =============================================================================
