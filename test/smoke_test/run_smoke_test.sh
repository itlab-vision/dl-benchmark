#!/bin/bash

omz_downloader --output_dir working_dir_smoke --cache_dir cache_dir_smoke      --name=mobilenet-v1-1.0-224-tf
omz_converter  --output_dir working_dir_smoke --download_dir working_dir_smoke --name=mobilenet-v1-1.0-224-tf --precisions FP32

python3 ../../src/benchmark/inference_benchmark.py -r results.csv --executor_type host_machine -c ./smoke_config.xml

success_tests=$(grep -o 'Success' results.csv | wc -l)
if [ $success_tests -ne 3 ]; then
    echo "There are should be 3 tests and all the tests should be passed"
    exit 1
fi
exit 0
