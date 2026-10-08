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

## Experiment 2: CPU-Based HorizontalPodAutoscaler

### Goal

Evaluate whether CPU utilization is an effective autoscaling signal
for a queue-based worker workload.

### Configuration

The HorizontalPodAutoscaler targets the worker Deployment.

- Minimum replicas: 1
- Maximum replicas: 10
- Target CPU utilization: 50%

### Workload

200 messages are published to RabbitMQ.

Each worker processes approximately one message per second.

### Expected Behavior

The RabbitMQ queue grows significantly.

However, the worker spends much of its processing time waiting rather
than performing CPU-intensive computation.

As a result, CPU utilization may remain below the HPA threshold even
while many messages are waiting.

### Observation

Record the observed:

- RabbitMQ queue length
- Worker CPU utilization
- Number of worker replicas

### Explanation

CPU utilization is an indirect measure of pending work.

For queue-driven applications, a large backlog can exist without
causing high CPU utilization.

Therefore, CPU-based autoscaling may not respond appropriately to this
type of workload.

### Conclusion

The experiment demonstrates why another scaling signal, such as
RabbitMQ queue length, may better represent the actual workload.