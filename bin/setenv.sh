#!/bin/bash

echo Searching OpenVINO environment
OpenVINO=$(find / -name setupvars.sh 2>/dev/null | grep /bin/setupvars.sh)
source $OpenVINO >/dev/null
echo OpenVINO environment initialized

echo Setting benchmark environment
export BENCHMARK_DIR=$(find / -name setenv.sh 2>/dev/null | grep openvino-dl-benchmark/bin/setenv.sh | rev | cut -c 15- | rev)
PYTHONPATH=$BENCHMARK_DIR
echo Benchmark environment initialized