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
#    - get_connection() establishes a connection to RabbitMQ using robust, env-driven credentials.
#      Now includes retry logic to avoid race conditions at startup.
#    - publish_event(topic, payload) sends a durable message to the
#      specified queue/topic, with the payload serialized as JSON.
#    - Always closes the connection after publishing to avoid resource leaks.
# =============================================================================

import pika
import os
import json
import time

def get_connection():
    """
    Establish a connection to the RabbitMQ broker using environment variables.
    Retries connection for up to 10 attempts (with 5s wait) for Docker race condition safety.
    Defaults ensure reliability in Docker, Azure, and other cloud CI/CD systems.
    """
    host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    port = int(os.getenv('RABBITMQ_PORT', 5672))
    user = os.getenv('RABBITMQ_USER', 'admin')
    password = os.getenv('RABBITMQ_PASS', 'password')
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
            print(f"[event_bus.py] Waiting for RabbitMQ... attempt {attempt+1}/10")
            time.sleep(5)
    raise Exception("Failed to connect to RabbitMQ after 10 attempts.")

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
