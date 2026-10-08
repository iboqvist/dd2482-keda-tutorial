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

## Experiment 3: KEDA RabbitMQ Autoscaling

### Goal

Scale the worker Deployment based directly on the number of pending messages in RabbitMQ.
Configuration
KEDA was configured with:

- RabbitMQ QueueLength trigger
- Queue: task_queue
- Target: 10 messages per worker
- Minimum replicas: 0
- Maximum replicas: 10
- Polling interval: 5 seconds
- Cooldown period: 30 seconds

### Workload

A large number of messages was published to RabbitMQ while the worker Deployment was scaled to zero.

### Observation

KEDA detected the RabbitMQ backlog and increased the number of worker replicas.
During the experiment, the number of replicas increased approximately as follows:

0 -> 1 -> 4 -> 8 -> 10

As the queue was processed, KEDA reduced the number of replicas again.
After the queue became empty and the cooldown period passed, the Deployment scaled back to zero.
Example behavior:

```text

Queue receives messages
        |
        v
KEDA detects queue length
        |
        v
0 -> multiple workers
        |
        v
Queue is processed in parallel
        |
        v
Queue becomes empty
        |
        v
Workers -> 0

```

### Conclusion

KEDA responds directly to the actual amount of pending work.
For this queue-based workload, RabbitMQ queue length is a more appropriate scaling signal than CPU utilization.

| Approach | Scaling Signal | Observed Behavior |
|---|---|---|
| No autoscaling | None | Always 1 worker |
| CPU-based HPA | CPU utilization | CPU stayed around 1%, so the worker did not scale |
| KEDA | RabbitMQ queue length | Workers scaled up with the backlog and returned to 0 when the queue was empty |

## Final Observation

The experiments show that the effectiveness of autoscaling depends strongly on choosing a metric that represents the actual workload.
For this application, CPU utilization does not represent the amount of pending work well, while RabbitMQ queue length directly reflects the number of jobs waiting to be processed.
