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
import time

def get_connection():
    """
    Establishes a robust blocking connection to RabbitMQ using environment variables,
    with retry logic to avoid service startup race conditions.
    Uses 'rabbitmq' as host (Docker Compose), with admin/password unless overridden.
    """
    host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    port = int(os.getenv("RABBITMQ_PORT", 5672))
    user = os.getenv("RABBITMQ_USER", "admin")
    password = os.getenv("RABBITMQ_PASS", "password")

    for attempt in range(10):
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host,
                    port=port,
                    credentials=pika.PlainCredentials(user, password)
                )
            )
        except pika.exceptions.AMQPConnectionError as e:
            print(f"[event_bus.py] Waiting for RabbitMQ... attempt {attempt + 1}/10. Error: {e}")
            time.sleep(5)
    raise Exception("Failed to connect to RabbitMQ after 10 attempts.")

def publish_event(topic, payload):
    """
    Publishes an event to the specified RabbitMQ queue/topic.
    - topic (str): The queue/topic to send to (e.g., 'rule.ingestion')
    - payload (dict): A JSON-serializable dictionary (event data)
    Ensures durability and reliability for all event-driven integrations.
    """
    connection = None
    try:
        connection = get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=topic, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=topic,
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
        )
        print(f"[event_bus.py] Published event to '{topic}': {payload}")
    except Exception as e:
        print(f"[event_bus.py] Failed to publish event to '{topic}': {e}")
        raise
    finally:
        if connection:
            try:
                connection.close()
            except Exception as e:
                print(f"[event_bus.py] Error closing RabbitMQ connection: {e}")

# =============================================================================
#  End of event_bus.py (simple, robust RabbitMQ publish utility)
# =============================================================================
