# =============================================================================
#  event_bus.py -- RabbitMQ Event Publishing Utility for IAC Analysis Service
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  DESCRIPTION:
#    - Provides helper functions to publish events from this microservice to RabbitMQ.
#    - Used for real-time dashboard updates and system observability.
#
#  KEY FUNCTIONS:
#    - get_connection: Creates a connection to RabbitMQ with universal credentials.
#    - publish_event: Publishes a JSON event payload to a named topic/queue.
#
#  USAGE:
#    - Import publish_event in your main Flask service file.
#    - Call publish_event(topic, payload) after completing any major pipeline step.
#
#  ENVIRONMENT:
#    - Assumes RabbitMQ is available at hostname 'rabbitmq' with user: admin, password: password.
#    - These credentials are set in your docker-compose.yml for all Python services.
# =============================================================================

import pika
import json

def get_connection():
    """
    Establish a new connection to RabbitMQ using shared service credentials.
    Returns a pika.BlockingConnection object.
    """
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('admin', 'password')
        )
    )

def publish_event(topic, payload):
    """
    Publishes a JSON event to the specified RabbitMQ queue.
    - topic (str): The name of the queue/topic (e.g., 'remediation.pipeline')
    - payload (dict): The event data to send (will be serialized as JSON)
    """
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=topic, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=topic,
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

# =============================================================================
#  End of event_bus.py (Reusable for all Python microservices)
# =============================================================================
