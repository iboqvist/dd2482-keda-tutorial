import os
import sys
import time

import pika


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "demo")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "demo")
QUEUE_NAME = os.getenv("QUEUE_NAME", "task_queue")


def connect():
    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD,
    )

    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials,
        )
    )


def main():
    message_count = int(sys.argv[1]) if len(sys.argv) > 1 else 100

    connection = connect()
    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
        arguments={"x-queue-type": "quorum"},
    )

    print(f"Sending {message_count} messages...")

    for i in range(message_count):
        message = f"job-{i + 1}"

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ),
        )

        if (i + 1) % 100 == 0:
            print(f"Sent {i + 1}/{message_count}")

    print("Finished sending messages.")

    connection.close()


if __name__ == "__main__":
    main()