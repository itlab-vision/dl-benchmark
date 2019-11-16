#!/bin/bash
echo "Run client script"
./client.sh $1
cd /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader
source ~/Documents/benchmark/OpenVINO_env/bin/activate

python3 -mpip install --user -r ./requirements.in

echo "Download models"
./downloader.py --all

echo "Convert to FP16"
./converter.py --all --precisions=FP16
echo "Convert to FP32"
./converter.py --all --precisions=FP32
echo "Convert to INT8"
./converter.py --all --precisions=INT8
