#!/bin/bash
set -e

MESSAGE_COUNT=${1:-100}

echo "Generating workload with ${MESSAGE_COUNT} messages..."

python app/producer.py "$MESSAGE_COUNT"