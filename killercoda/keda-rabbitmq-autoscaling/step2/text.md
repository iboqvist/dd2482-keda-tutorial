# Experiment 1: No Autoscaling

In the first experiment, we will observe how the application behaves
without any autoscaling mechanism. This will then be used as a benchmark to compare the autoscaling options against.

The worker Deployment is configured with exactly one replica.

## 1. Set and verify the worker count

`kubectl scale deployment worker --replicas=1`{{exec}}

`kubectl get deployment worker`{{exec}}

There should be exactly one worker replica.

## 2. Generate workload

The following step creates a new pod running a RabbitMQ producer. The newly created producer is then called upon to generate 100 messages. 

A queue named `task_queue` is declared, which the newly published messages are routed to through the default exchange. 

`bash scripts/generate-load.sh 100`{{exec}}

## 3. Inspect the RabbitMQ queue

Recall from the previous step that each message takes a worker one second to process. As soon as the 100 messages are routed to the queue, the sole worker starts processing messages.

Check how many messages are waiting:

`kubectl exec deployment/rabbitmq -- rabbitmqctl list_queues name messages_ready messages_unacknowledged`{{exec}}

There should be two columns: `messages_ready` and `messages_unacknowledged`. The former represents messages waiting in the queue, while the latter represents messages currently being processed. 

You should expect to see a little under 100 messages under `messages_ready` in `task_queue`, depending on how long it's been since you ran the last step. As we only have one worker, `messages_unacknowledged` will stay constant at 1 while messages are being processed.

## 4. Inspect the workers

`kubectl get pods -l app=worker`{{exec}}

Even though RabbitMQ contains many pending jobs, Kubernetes still runs
only one worker.

Wait a little and inspect the queue again:

`sleep 20 && kubectl exec deployment/rabbitmq -- rabbitmqctl list_queues name messages_ready messages_unacknowledged`{{exec}}

The queue is decreasing because the worker processes messages, but the
number of worker replicas remains unchanged.

## Why?

Kubernetes does not automatically know that the RabbitMQ queue
represents pending work.

Without an autoscaling mechanism, the Deployment always keeps the
configured number of replicas.

```text
Large RabbitMQ backlog
        |
        v
     1 worker
        |
        v
Sequential processing
```

In the next experiment, we will enable Kubernetes HorizontalPodAutoscaler
and use CPU utilization as the scaling signal.
