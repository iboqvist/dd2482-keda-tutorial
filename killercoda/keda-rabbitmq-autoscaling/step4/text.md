# Experiment 3: Event-Driven Autoscaling with KEDA

The previous experiment showed that CPU utilization does not always
represent the amount of pending work.

KEDA allows Kubernetes workloads to scale using external event sources.

For this application, we will use the RabbitMQ queue length directly.

## 1. Install KEDA

`bash scripts/install-keda.sh`{{exec}}

Verify that KEDA is running:

`kubectl get pods -n keda`{{exec}}

## 2. Configure RabbitMQ authentication

Apply the RabbitMQ credentials:

`kubectl apply -f kubernetes/base/rabbitmq-secret.yaml`{{exec}}

Create the KEDA TriggerAuthentication:

`kubectl apply -f kubernetes/keda/trigger-authentication.yaml`{{exec}}

## 3. Create the ScaledObject

`kubectl apply -f kubernetes/keda/scaledobject.yaml`{{exec}}

Inspect it:

`kubectl get scaledobject`{{exec}}

The ScaledObject should eventually report:

```text
READY   True
```

KEDA also creates an HPA automatically:

`kubectl get hpa`{{exec}}

The scaling configuration uses:

- RabbitMQ queue: `task_queue`
- Target: 10 messages per worker
- Minimum replicas: 0
- Maximum replicas: 10
- Polling interval: 5 seconds
- Cooldown period: 30 seconds

## 4. Observe scale-to-zero

Because there is currently no work, KEDA can remove the worker pods.

`sleep 35 && kubectl get deployment worker`{{exec}}

`kubectl get pods -l app=worker`{{exec}}

The Deployment may now have zero worker replicas.

```text
No messages
     |
     v
0 workers
```

## 5. Generate workload

Publish 100 messages:

`bash scripts/generate-load.sh 100`{{exec}}

Give KEDA a few seconds to detect the queue:

`sleep 15 && kubectl get pods -l app=worker`{{exec}}

Inspect the HPA:

`kubectl get hpa`{{exec}}

Inspect RabbitMQ:

`kubectl exec deployment/rabbitmq -- rabbitmqctl list_queues name messages_ready messages_unacknowledged`{{exec}}

KEDA should create multiple workers.

```text
100 messages
     |
     v
RabbitMQ queue
     |
     v
KEDA
     |
     v
Multiple workers
```

The workers can now process jobs in parallel.

## 6. Observe scale-down

Once the queue becomes empty, KEDA no longer needs the workers.

Wait for the workload and cooldown period:

`sleep 45 && kubectl get deployment worker`{{exec}}

Inspect the worker pods again:

`kubectl get pods -l app=worker`{{exec}}

The worker Deployment should eventually return to zero replicas.

## Why is this different?

KEDA uses the amount of pending work itself as the scaling signal.

```text
Queue grows
   |
   v
KEDA detects backlog
   |
   v
More workers
   |
   v
Queue decreases
   |
   v
Workers scale down
```

For this queue-driven workload, queue length represents the workload
more directly than CPU utilization.