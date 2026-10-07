import sys

import pika

# Establish connection with RabbitMQ server
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost", credentials=pika.PlainCredentials("demo", "demo")
    )
)
channel = connection.channel()

# Create a task_queue queue
channel.queue_declare(
    queue="task_queue", durable=True, arguments={"x-queue-type": "quorum"}
)

# Send a message
message = " ".join(sys.argv[1:]) or "Hello world!"
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=message,
    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
)
print(f"Sent {message}")

# Gently close connection
connection.close()
