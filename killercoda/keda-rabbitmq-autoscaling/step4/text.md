# Experiment 3: KEDA Autoscaling

In this experiment, we will install KEDA and configure a RabbitMQ
QueueLength trigger.

KEDA will scale the worker Deployment according to the number of
pending messages.