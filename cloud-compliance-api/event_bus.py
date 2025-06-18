# event_bus.py
import pika
import json

def get_connection():
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('admin', 'password')
        )
    )

def publish_event(topic, payload):
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
