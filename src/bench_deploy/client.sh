#!/bin/bash

echo "Update components"
#apt-get update

echo "Delete old components"
rm -r /home/itmm/inference_engine_samples_build
rm -r /home/itmm/openvino_models

cd ~/Downloads/
wget $1

arch_name="$(ls | grep ".tgz")"
tar -xvzf $arch_name
cd "$(basename $arch_name .tgz)"
sed -i 's/=decline/=accept/' silent.cfg

echo "Delete old openvino"
sed -i 's/=install/=uninstall/' silent.cfg
./install.sh --silent silent.cfg

source ~/Documents/benchmark/OpenVINO_env/bin/activate

echo "Install new openvino"
sed -i 's/=uninstall/=install/' silent.cfg
sudo ./install.sh --silent silent.cfg

echo "Install openvino dependencies"
cd /opt/intel/openvino/install_dependencies
sudo ./install_openvino_dependencies.sh -E
