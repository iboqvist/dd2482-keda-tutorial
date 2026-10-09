# Tutorial Complete

You have compared three scaling strategies for a queue-based Kubernetes
workload:

- Fixed replicas
- CPU-based HorizontalPodAutoscaler
- RabbitMQ event-driven autoscaling with KEDA

The experiments demonstrate that choosing an appropriate workload
metric is essential for effective autoscaling.

For this workload, RabbitMQ queue length represents pending work more
directly than CPU utilization.