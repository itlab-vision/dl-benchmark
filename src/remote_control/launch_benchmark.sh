#!/bin/bash
source /opt/intel/computer_vision_sdk_2018.4.420/bin/setupvars.sh
cd /home/itmm/Documents/openvino-dl-benchmark/src/benchmark/
tablepath="/home/itmm/Documents/openvino-dl-benchmark/src/remote_control/result_table.csv"
python3 inference_benchmark.py -c benchmark_configuration.xml -f $tablepath


