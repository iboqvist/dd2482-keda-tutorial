# Experiment 1: No Autoscaling

In the first experiment, we will observe how the application behaves
without any autoscaling mechanism.

The worker Deployment is configured with exactly one replica.

## 1. Verify the worker count

`kubectl scale deployment worker --replicas=1`{{exec}}

`kubectl get deployment worker`{{exec}}

There should be exactly one worker replica.

## 2. Generate workload

Publish 100 messages to RabbitMQ:

`bash scripts/generate-load.sh 100`{{exec}}

## 3. Inspect the RabbitMQ queue

Check how many messages are waiting:

`kubectl exec deployment/rabbitmq -- rabbitmqctl list_queues name messages_ready messages_unacknowledged`{{exec}}

You should see messages waiting in `task_queue`.

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