#!/bin/bash

. ./utils.sh

mkdir -p working_dir_smoke/spektral
curl -o working_dir_smoke/spektral/model.keras https://raw.githubusercontent.com/ArchiMikael/spektral/main/model.keras

result_file="results_benchmark_spektral.csv"
[ -f $result_file ] && rm $result_file
smoke_config_file="smoke_config_spektral.xml"
smoke_tests_count=$(grep -io '<Test>' "$smoke_config_file" | wc -l)

python ../../src/benchmark/inference_benchmark.py -r $result_file --executor_type host_machine -c $smoke_config_file
check_exit_code inference_benchmark
check_results_file $result_file $smoke_tests_count

exit $return_value
