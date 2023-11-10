#!/bin/bash

. ./utils.sh

omz_downloader --output_dir working_dir_smoke --cache_dir cache_dir_smoke      --name=mobilenet-v1-1.0-224-tf,efficientnet-b0-pytorch,googlenet-v1
omz_converter  --output_dir working_dir_smoke --download_dir working_dir_smoke --name=mobilenet-v1-1.0-224-tf,efficientnet-b0-pytorch --precisions FP32
cd working_dir_smoke/
python3 ../../../src/model_converters/tvm_converter/pytorch_to_tvm_converter.py \
                                                                                -mn efficientnet_b0 \
                                                                                -w public/efficientnet-b0-pytorch/efficientnet-b0.pth \
                                                                                -is 1 3 224 224
python3 ../../../src/model_converters/tvm_converter/mxnet_to_tvm_converter.py -mn alexnet -is 1 3 224 224
python3 ../../../src/model_converters/tvm_converter/caffe_to_tvm_converter.py -mn googlenet-v1 -is 1 3 227 227 \
                                                                              -m public/googlenet-v1/googlenet-v1.prototxt \
                                                                              -w public/googlenet-v1/googlenet-v1.caffemodel
cd ../

result_file="results_benchmark.csv"
[ -f $result_file ] && rm $result_file
smoke_config_file="smoke_config.xml"
smoke_tests_count=$(grep -io '<Test>' "$smoke_config_file" | wc -l)

python3 ../../src/benchmark/inference_benchmark.py -r $result_file --executor_type host_machine -c $smoke_config_file
check_exit_code inference_benchmark
check_results_file $result_file $smoke_tests_count

exit $return_value
