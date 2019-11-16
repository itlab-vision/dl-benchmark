#!/bin/bash

echo "Update components"
yes | apt-get update

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

echo "Setting vars"
source /opt/intel/openvino/bin/setupvars.sh

echo "Configurate model_optimizer"
cd /opt/intel/openvino/deployment_tools/model_optimizer/install_prerequisites
sudo ./install_prerequisites.sh

echo "Test run"
cd /opt/intel/openvino/deployment_tools/demo
./demo_squeezenet_download_convert_run.sh
