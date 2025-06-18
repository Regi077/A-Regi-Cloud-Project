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
#    - Use the same credentials and host as defined in docker-compose.yml.
# =============================================================================

import pika
import json

def get_connection():
    """
    Establish a connection to the RabbitMQ broker.
    Uses fixed host/credentials for project-wide consistency.
    """
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',  # Must match docker-compose service name
            credentials=pika.PlainCredentials('admin', 'password')
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
