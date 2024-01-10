#!/bin/bash

mkdir -p working_dir_smoke/resnet50
curl -o working_dir_smoke/resnet50/resnet50.so https://raw.githubusercontent.com/itlab-vision/itlab-vision-dl-benchmark-models/main/models/classification/resnet50-tvm-optimized/resnet50.so
cd working_dir_smoke/
converters="../../../src/model_converters/tvm_converter"
python3 $converters/tvm_converter.py \
                                      -mn efficientnet_b0 \
                                      -w public/efficientnet-b0-pytorch/efficientnet-b0.pth \
                                      -is 1 3 224 224 \
                                      -op public/efficientnet-b0-pytorch/ \
                                      -f pytorch
python3 $converters/tvm_converter.py \
                                      -mn alexnet \
                                      -is 1 3 224 224 \
                                      -op public/alexnet/ \
                                      -f mxnet
cd ../