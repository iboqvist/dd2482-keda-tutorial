import time

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


# Define message callback
def callback(ch, method, properties, body):
    print(f"Received {body.decode()}")
    time.sleep(body.count(b"."))
    print("Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Tell sender to wait for ack before queueing another task
channel.basic_qos(prefetch_count=1)

# Set callback for messages from task_queue
channel.basic_consume(queue="task_queue", on_message_callback=callback)

try:
    # Wait for messages
    print("Waiting for messages...")
    channel.start_consuming()
except KeyboardInterrupt:
    # Gently close connection
    connection.close()
