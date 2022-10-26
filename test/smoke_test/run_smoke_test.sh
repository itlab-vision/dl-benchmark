#!/bin/bash

omz_downloader --output_dir working_dir_smoke --cache_dir cache_dir_smoke      --name=mobilenet-v1-1.0-224-tf
omz_converter  --output_dir working_dir_smoke --download_dir working_dir_smoke --name=mobilenet-v1-1.0-224-tf --precisions FP32

result_file="results.csv"
[ -f $result_file ] && rm $result_file

python3 ../../src/benchmark/inference_benchmark.py -r results.csv --executor_type host_machine -c ./smoke_config.xml
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "inference_benchmark.py exited with non-zero code: ${retVal}"
fi

if [ ! -f $result_file ]; then
    echo "File $result_file not exist!"
    retVal=128
else
    success_tests=$(grep -o 'Success' results.csv | wc -l)
    failed_tests=$(grep Failed results.csv)
    if [ $success_tests -ne 3 ]; then
        echo "There are should be 3 tests and all the tests should be passed"
        echo "Failed tests:"
        echo $failed_tests
        retVal=255
    fi
fi
exit $retVal
