import os
import time

import pika


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "demo")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "demo")
QUEUE_NAME = os.getenv("QUEUE_NAME", "task_queue")

PROCESSING_TIME = float(os.getenv("PROCESSING_TIME", "1"))


credentials = pika.PlainCredentials(
    RABBITMQ_USER,
    RABBITMQ_PASSWORD,
)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=credentials,
    )
)

channel = connection.channel()

channel.queue_declare(
    queue=QUEUE_NAME,
    durable=True,
    arguments={"x-queue-type": "quorum"},
)


def callback(ch, method, properties, body):
    message = body.decode()

    print(f"Processing {message}")

    time.sleep(PROCESSING_TIME)

    print(f"Finished {message}")

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue=QUEUE_NAME,
    on_message_callback=callback,
)

print("Worker waiting for messages...")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    connection.close()