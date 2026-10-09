# Compare the Results

You have now tested three different approaches to scaling the same
queue-based workload.

## Experiment 1 — No Autoscaling

```text
RabbitMQ backlog
       |
       v
    1 worker
```

The number of workers remains fixed regardless of how many messages are
waiting.

## Experiment 2 — CPU-Based HPA

```text
RabbitMQ backlog
       |
       v
Worker CPU ~ low
       |
       v
HPA does not significantly scale
```

CPU utilization does not accurately represent the pending work because
the worker is primarily I/O-bound.

## Experiment 3 — KEDA

```text
RabbitMQ backlog
       |
       v
QueueLength metric
       |
       v
KEDA
       |
       v
Multiple workers
```

KEDA reacts directly to the number of pending messages.

## Comparison

| Approach | Scaling signal | Behavior |
|---|---|---|
| No autoscaling | None | Worker count remains fixed |
| Kubernetes HPA | CPU utilization | Low CPU prevents useful scaling |
| KEDA | RabbitMQ queue length | Workers scale according to pending work |

## Design Decisions

### Why RabbitMQ?

RabbitMQ provides a simple queue-based workload where pending work can
be observed directly.

### Why KEDA?

KEDA supports event-driven autoscaling and can use RabbitMQ queue length
as an external scaling signal.

### Why not CPU alone?

CPU utilization is an indirect metric.

For I/O-bound systems, a large workload may exist even while CPU usage
is low.

### Why scale to zero?

When the queue is empty, no worker resources are required.

KEDA can therefore reduce the worker Deployment to zero replicas and
create workers again when new work arrives.

## When is KEDA useful?

KEDA is particularly useful for:

- Message queue consumers
- Asynchronous workers
- Event-driven architectures
- Workloads with long idle periods
- Systems where CPU does not represent pending work well

## When might normal HPA be enough?

CPU-based HPA can be simpler and appropriate when CPU or memory usage
closely represents the workload, such as many compute-intensive
services.

## Final Result

The experiments demonstrate an important autoscaling principle:

> The effectiveness of autoscaling depends on choosing a metric that
> represents the actual workload.

For this application, RabbitMQ queue length is a better scaling signal
than CPU utilization.