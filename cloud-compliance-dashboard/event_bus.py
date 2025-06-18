import pika
import json

def get_connection():
    # Use your specified RabbitMQ credentials
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('admin', 'password')
        )
    )

def consume_events(topic, handler):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=topic, durable=True)
    for method_frame, properties, body in channel.consume(topic, inactivity_timeout=1):
        if body:
            handler(json.loads(body))
            channel.basic_ack(method_frame.delivery_tag)

