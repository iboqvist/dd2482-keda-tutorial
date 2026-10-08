#!/bin/bash
set -e

KEDA_VERSION="2.21.0"

echo "Installing KEDA ${KEDA_VERSION}..."

kubectl apply --server-side \
  -f "https://github.com/kedacore/keda/releases/download/v${KEDA_VERSION}/keda-${KEDA_VERSION}.yaml"

echo "Waiting for KEDA..."
kubectl rollout status deployment/keda-operator -n keda --timeout=120s

echo "KEDA installed."