#!/bin/bash

echo "Update components"
#apt-get update

rm -r /home/itmm/inference_engine_samples_build
rm -r /home/itmm/openvino_models

cd ~/Downloads/
wget $1

arch_name="$(ls | grep ".tgz")"
tar -xvzf $arch_name
cd "$(basename $arch_name .tgz)"
sudo ./install.sh