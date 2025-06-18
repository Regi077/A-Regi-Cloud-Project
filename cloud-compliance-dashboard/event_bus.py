# =============================================================================
# cloud-compliance-dashboard/event_bus.py
#
# Author: Reginald
# Last updated: 18th June 2025
#
# Description:
#   Utility module to connect to RabbitMQ, subscribe to pipeline event topics,
#   and relay events into the dashboard backend.
#
#   - get_connection(): Helper to establish a connection to RabbitMQ using
#     universal project credentials.
#   - consume_events(): Listen to a specified queue, passing each event to
#     the given handler function (used by the dashboard for live updates).
#
# Notes:
#   - Connection settings must match those in your docker-compose.yml.
#   - If RabbitMQ credentials change, update them here.
#   - Designed for safe and simple event consumption (no publishing here).
# =============================================================================

import pika
import json

def get_connection():
    """
    Establish and return a blocking connection to RabbitMQ.
    Credentials and host must match those set in docker-compose.yml.
    """
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',  # Service name from docker-compose
            credentials=pika.PlainCredentials('admin', 'password')
        )
    )

def consume_events(topic, handler):
    """
    Continuously consume messages from the given RabbitMQ queue (topic).
    For each message, decode the payload and pass to the provided handler.

    Args:
        topic (str): The RabbitMQ queue name (e.g., "rule.ingestion").
        handler (callable): A function to call for every received event.

    Usage:
        consume_events("rule.ingestion", dashboard_event_handler)
    """
    connection = get_connection()
    channel = connection.channel()
    # Ensure the queue exists and is durable (persists through restarts)
    channel.queue_declare(queue=topic, durable=True)
    # Begin consuming events; inactivity_timeout ensures we don't hang forever
    for method_frame, properties, body in channel.consume(topic, inactivity_timeout=1):
        if body:
            # Convert bytes to dict and pass to handler (e.g., emit via SocketIO)
            handler(json.loads(body))
            # Acknowledge message so it's removed from the queue
            channel.basic_ack(method_frame.delivery_tag)
    # (Note: connection is left open for the daemon thread's lifecycle)
