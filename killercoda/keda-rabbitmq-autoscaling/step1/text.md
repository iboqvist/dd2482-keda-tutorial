# Deploy the Queue-Based Application

In this step, we will deploy RabbitMQ and a single worker inside Kubernetes.

RabbitMQ will store pending jobs in the `task_queue`, while the worker will consume and process them.

## 1. Move into the project directory

`cd /root/dd2482-keda-tutorial`{{exec}}

## 2. Deploy RabbitMQ

Create the RabbitMQ credentials:

`kubectl apply -f kubernetes/base/rabbitmq-secret.yaml`{{exec}}

Deploy RabbitMQ:

`kubectl apply -f kubernetes/base/rabbitmq-deployment.yaml`{{exec}}

Create the RabbitMQ Service:

`kubectl apply -f kubernetes/base/rabbitmq-service.yaml`{{exec}}

Wait until RabbitMQ is ready:

`kubectl rollout status deployment/rabbitmq --timeout=120s`{{exec}}

## 3. Deploy the worker

Deploy one worker:

`kubectl apply -f kubernetes/base/worker-deployment.yaml`{{exec}}

Wait until the worker is ready:

`kubectl rollout status deployment/worker --timeout=120s`{{exec}}

## 4. Verify the deployment

Inspect the running pods:

`kubectl get pods`{{exec}}

You should see both RabbitMQ and the worker running:

```text
rabbitmq-...   1/1   Running
worker-...     1/1   Running
```

Inspect the RabbitMQ Service:

`kubectl get svc rabbitmq`{{exec}}

Finally, check the worker logs:

`kubectl logs deployment/worker`{{exec}}

The worker should report that it is waiting for messages.

## What happened?

The application now has two main components:

```text
RabbitMQ
   |
   v
Worker
```

RabbitMQ stores pending jobs, and the worker continuously waits for new messages to process.

In the next step, we will generate a workload and observe what happens when no autoscaling mechanism is configured.