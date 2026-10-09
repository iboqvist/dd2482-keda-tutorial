# Kubernetes Event-Driven Autoscaling with KEDA and RabbitMQ

In this tutorial, you will explore how different autoscaling strategies
behave for a queue-based workload running on Kubernetes.

The application consists of a Python producer, RabbitMQ, and worker pods.

You will compare three approaches:

1. No autoscaling
2. CPU-based Kubernetes HorizontalPodAutoscaler
3. Event-driven autoscaling using KEDA and RabbitMQ queue length

## Architecture

```text
Producer
   |
   v
RabbitMQ
   |
   v
Workers
   ^
   |
  KEDA

```

## Learning Outcomes

After completing this tutorial, you will be able to:

- Explain why CPU utilization may not represent the workload of an
  I/O-bound queue consumer.
- Deploy RabbitMQ and worker applications on Kubernetes.
- Configure a CPU-based HorizontalPodAutoscaler.
- Configure KEDA to monitor a RabbitMQ queue.
- Observe scale-to-zero and event-driven scaling.
- Compare CPU-based and event-driven autoscaling strategies.