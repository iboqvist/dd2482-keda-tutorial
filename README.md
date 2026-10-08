# Kubernetes Event-Driven Autoscaling with KEDA and RabbitMQ

Executable DevOps tutorial demonstrating different approaches to
autoscaling queue-based workloads in Kubernetes.

## Overview

The tutorial compares three approaches:

1. No autoscaling
2. CPU-based Kubernetes HorizontalPodAutoscaler
3. Event-driven autoscaling with KEDA and RabbitMQ

## Architecture 

The application consists of:

- A Python producer that creates jobs
- RabbitMQ as a message broker
- Python workers that process jobs
- Kubernetes for orchestration
- KEDA for event-driven autoscaling

```text
Producer
   |
   v
RabbitMQ
   |
   v
Workers
   ^
   |
  KEDA

```

## Learning Outcomes

After completing this tutorial, you will be able to:

- Explain the limitations of CPU-based autoscaling for queue workloads.
- Deploy RabbitMQ on Kubernetes.
- Deploy worker applications on Kubernetes.
- Configure a CPU-based HorizontalPodAutoscaler.
- Install and configure KEDA.
- Scale workers based on RabbitMQ queue length.
- Compare CPU-based and event-driven autoscaling.

## Project Structure

```text
app/
kubernetes/
scripts/
docs/
killercoda/

```

## Components

### Producer

Creates jobs and sends them to RabbitMQ.

### RabbitMQ

Stores pending jobs until workers are able to process them.

### Worker

Consumes messages from RabbitMQ and simulates processing work.

### KEDA

Observes RabbitMQ queue length and exposes an external metric to
Kubernetes.

### Kubernetes HPA

Adjusts the number of worker replicas based on the metric supplied
by KEDA.
