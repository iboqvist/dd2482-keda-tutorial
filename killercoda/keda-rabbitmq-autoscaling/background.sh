#!/bin/bash
set -e

cd /root

if [ ! -d "dd2482-keda-tutorial" ]; then
  git clone https://github.com/iboqvist/dd2482-keda-tutorial.git
fi

cd /root/dd2482-keda-tutorial
git checkout main