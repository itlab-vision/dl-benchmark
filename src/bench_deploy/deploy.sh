#!/bin/bash

echo "Start on all machines"
file="config.txt"
for var in $(cat $file)
do
    ssh 
    echo "Download repos"
    cd ~/Documents/
    git clone https://github.com/itlab-vision/openvino-dl-benchmark.git
    cd openvino-dl-benchmark/src/bench_deploy/
    nohup ./client.sh $1 &
done

echo "Run client script"
sudo ./client.sh $1
cd /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader
source ~/Documents/benchmark/OpenVINO_env/bin/activate

python3 -mpip install --user -r ./requirements.in

echo "Download models"
sudo ./downloader.py --all

echo "Setting vars"
source /opt/intel/openvino/bin/setupvars.sh

echo "Convert to FP16"
sudo ./converter.py --all --precisions=FP16 --mo ../../../model_optimizer/mo.py
echo "Convert to FP32"
sudo ./converter.py --all --precisions=FP32 --mo ../../../model_optimizer/mo.py
echo "Convert to INT8"
sudo ./converter.py --all --precisions=INT8 --mo ../../../model_optimizer/mo.py
