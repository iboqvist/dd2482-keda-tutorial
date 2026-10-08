# Deploy the Queue-Based Application

We will first deploy RabbitMQ and a single worker.

The producer sends jobs to the `task_queue`. Workers consume these jobs
and simulate an I/O-bound workload.

## Move into the project directory

`cd /root/dd2482-keda-tutorial`{{exec}}

## Deploy RabbitMQ

First, deploy the credentials:

`kubectl apply -f kubernetes/base/rabbitmq-secret.yaml`{{exec}}

Deploy RabbitMQ:

`kubectl apply -f kubernetes/base/rabbitmq-deployment.yaml`{{exec}}

Create the RabbitMQ Service:

`kubectl apply -f kubernetes/base/rabbitmq-service.yaml`{{exec}}

## Wait for RabbitMQ

Wait until the RabbitMQ Deployment is ready:

`kubectl rollout status deployment/rabbitmq --timeout=120s`{{exec}}

Now inspect the resources:

`kubectl get pods`{{exec}}

`kubectl get svc rabbitmq`{{exec}}

RabbitMQ should now be running inside the Kubernetes cluster.

In the next step, we will use the worker application to process messages from the queue.