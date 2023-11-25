#!/bin/bash

. ./utils.sh

omz_downloader --output_dir working_dir_smoke --cache_dir cache_dir_smoke      --name=mobilenet-v1-1.0-224-tf,efficientnet-b0-pytorch
omz_converter  --output_dir working_dir_smoke --download_dir working_dir_smoke --name=mobilenet-v1-1.0-224-tf,efficientnet-b0-pytorch --precisions FP32

. ./run_tvm_model_converters.sh

result_file="results_benchmark.csv"
[ -f $result_file ] && rm $result_file
smoke_config_file="smoke_config.xml"
smoke_tests_count=$(grep -io '<Test>' "$smoke_config_file" | wc -l)

python3 ../../src/benchmark/inference_benchmark.py -r $result_file --executor_type host_machine -c $smoke_config_file
check_exit_code inference_benchmark
check_results_file $result_file $smoke_tests_count

exit $return_value
