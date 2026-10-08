# Autoscaling Experiments

## Experiment 1: No Autoscaling

### Goal

Demonstrate how a fixed number of workers handles an increasing
RabbitMQ workload when no autoscaling mechanism is configured.

### Configuration

The worker Deployment runs with:

```yaml
replics: 1

```

Each worker processes one message approximately every second.

### Workload

100 messages are published to the RabbitMQ task_queue.
Expected Behavior
Kubernetes maintains exactly one worker replica regardless of the
number of pending messages.
As a result, messages accumulate in RabbitMQ and are processed
sequentially.

## Observation

```text
RabbitMQ queue
100
 ↓
80
 ↓
60
 ↓
40
 ↓
20
 ↓
0

Worker replicas: 1

```

## Conclusion

Without an autoscaling mechanism, Kubernetes does not react to the
amount of pending work in RabbitMQ.
