# Experiment 1: No Autoscaling

In this experiment, we will generate a RabbitMQ backlog while keeping
the worker Deployment fixed at one replica.

We will observe that Kubernetes does not react to the queue length
without an autoscaling mechanism.