#!/bin/bash
set -e

MESSAGE_COUNT=${1:-100}
IMAGE="ghcr.io/iboqvist/dd2482-keda-app:latest"
POD_NAME="load-generator"

echo "Generating ${MESSAGE_COUNT} messages..."

kubectl delete pod "${POD_NAME}" --ignore-not-found --wait=true >/dev/null

kubectl run "${POD_NAME}" \
  --restart=Never \
  --image="${IMAGE}" \
  --env="RABBITMQ_HOST=rabbitmq" \
  --command -- \
  python producer.py "${MESSAGE_COUNT}"

kubectl logs -f "${POD_NAME}"

echo "Workload generated."