# Experiment 2: CPU-Based HorizontalPodAutoscaler

Kubernetes HorizontalPodAutoscaler (HPA) can automatically change the
number of replicas depending on resource utilization. This autoscaling is implemented as a control loop. Metrics are read, compared against a target, and the replica count is scaled accordingly. 

By default, Kubernetes provides two metrics: CPU utilization and memory utilization. In this experiment, we will use CPU utilization.

Before starting, reset the queue from the previous experiment:

`kubectl exec deployment/rabbitmq -- rabbitmqctl purge_queue task_queue`{{exec}}

`kubectl scale deployment worker --replicas=1`{{exec}}

## 1. Install Metrics Server

For HPA to scale on CPU usage metrics, we need to pull down and apply the latest Metrics Server image:

`kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`{{exec}}

Allow the Metrics Server to connect to the kubelet without verifying certificates:

`kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'`{{exec}}

Wait until Metrics Server is ready:

`kubectl rollout status deployment/metrics-server -n kube-system --timeout=120s`{{exec}}

Wait for metrics to become available:

`sleep 15 && kubectl top pods`{{exec}}

## 2. Enable CPU-based autoscaling

We have defined a configuration file to connect the CPU metrics from Metrics Server into HPA. Apply the configuration:

`kubectl apply -f kubernetes/hpa/worker-hpa.yaml`{{exec}}

Inspect the HPA instance:

`kubectl get hpa`{{exec}}

The HPA is configured with:

- Minimum replicas: 1
- Maximum replicas: 10
- CPU target: 50%

## 3. Generate a larger workload

Now that we've configured HPA to scale on CPU utilization, let's generate a larger workload compared to the previous step and see what happens. Start with 200 messages:

`bash scripts/generate-load.sh 200`{{exec}}

Now wait a few seconds and inspect the CPU utilization:

`sleep 15 && kubectl top pods`{{exec}}

Inspect the HPA:

`kubectl get hpa`{{exec}}

Inspect the RabbitMQ backlog:

`kubectl exec deployment/rabbitmq -- rabbitmqctl list_queues name messages_ready messages_unacknowledged`{{exec}}

## What happened?

RabbitMQ may contain a large number of pending messages, while the worker
CPU utilization remains very low.

The worker simulates an I/O-bound workload and spends most of its time
waiting rather than performing CPU-intensive computation.

Therefore:

```text
Large queue
   |
   v
Worker waits for I/O
   |
   v
Low CPU utilization
   |
   v
HPA does not scale
```

CPU utilization is therefore not a good representation of the pending
work for this workload.

## Reset the experiment

Remove the HPA:

`kubectl delete -f kubernetes/hpa/worker-hpa.yaml`{{exec}}

Remove the remaining messages so the next experiment starts clean:

`kubectl exec deployment/rabbitmq -- rabbitmqctl purge_queue task_queue`{{exec}}

Return to one worker:

`kubectl scale deployment worker --replicas=1`{{exec}}

In the next experiment, we will scale directly from RabbitMQ queue length.
