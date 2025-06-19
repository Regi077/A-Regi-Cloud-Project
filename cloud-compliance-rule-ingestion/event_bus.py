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
#    - get_connection(): Creates a robust connection to the RabbitMQ broker using
#      environment variables (Docker-ready, secure, future-proof, with retry logic).
#    - publish_event(): Publishes a JSON-serializable payload to a named queue
#      (topic), with durability (message will survive broker restarts).
#
#  USAGE:
#    - Import and call publish_event("queue_name", {...}) from your pipeline code
#
#  CONFIGURATION:
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
        except pika.exceptions.AMQPConnectionError:
            print(f"[event_bus.py] Waiting for RabbitMQ... attempt {attempt + 1}/10")
            time.sleep(5)
    raise Exception("Failed to connect to RabbitMQ after 10 attempts.")

def publish_event(topic, payload):
    """
    Publishes an event to the specified RabbitMQ queue/topic.
    - topic (str): The queue/topic to send to (e.g., 'rule.ingestion')
    - payload (dict): A JSON-serializable dictionary (event data)
    Ensures durability and reliability for all event-driven integrations.
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
