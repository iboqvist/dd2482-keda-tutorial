# Kubernetes Event-Driven Autoscaling with KEDA and RabbitMQ

## Problem

One of the major benefits of Kubernetes compared to Docker and similar container orchestration tools is the support for scaling deployments to meet demand. 

Unlike Docker, where the only (built-in) lever you have is vertical scaling (or increasing container resources), Kubernetes supports horizontal scaling (or increasing the number of containers). This is often a really useful tool for ensuring that capacity scales with demand. 

In Kubernetes, horizontal scaling is achieved through an object called a HorizontalPodAutoscaler. By default, this scaler supports CPU and memory usage metrics. However, not all tasks scale with CPU or memory usage. 

Imagine a mail server receiving 100 emails at once. Each pod can only parse one email at a time. This task would be limited by disk performance, while the CPU and memory utilization metrics will stay low. In this situation, you might benefit from having other metrics to scale on.

## Solution

What if you could link your API, database, or message queue into HorizontalPodAutoscaler's metrics endpoint and scale based on demand? 

This is where KEDA, a Kubernetes-based Event Driven Autoscaler comes in. It supports a range of different integrations with different tools and services, among those PostgreSQL, Redis, and RabbitMQ. 

The usage information from these services are fed back into HorizontalPodAutoscaler to scale your workload all the way from hundreds to zero running pods based on actual demand and utilization.

## Overview

In this tutorial, you will explore how different autoscaling strategies behave for a queue-based workload running on Kubernetes. 

The application consists of a Python producer, RabbitMQ, and worker pods.

You will compare three approaches:

1. No autoscaling
2. CPU-based Kubernetes HorizontalPodAutoscaler
3. Event-driven autoscaling using KEDA and RabbitMQ queue length

## Architecture

```text
Producer
   |
   v
RabbitMQ ---|
   |        |
   v        v
Workers  Metrics
   ^        |
   |        |
  KEDA <-----

```

## Prerequisites

- A basic understanding of (Kubernetes)[https://kubernetes.io/docs/home/]

## Learning Outcomes

After completing this tutorial, you will be able to:

- Explain why CPU utilization may not represent the workload of an
  I/O-bound queue consumer.
- Deploy RabbitMQ and worker applications on Kubernetes.
- Configure a CPU-based HorizontalPodAutoscaler.
- Configure KEDA to monitor a RabbitMQ queue.
- Observe scale-to-zero and event-driven scaling.
- Compare CPU-based and event-driven autoscaling strategies.
