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

echo "Install old openvino"
sed -i 's/=uninstall/=install/' silent.cfg
./install.sh --silent silent.cfg

cd /opt/intel/openvino/install_dependencies
./install_openvino_dependencies.sh -E
source /opt/intel/openvino/bin/setupvars.sh
cd /opt/intel/openvino/deployment_tools/model_optimizer/install_prerequisites
./install_prerequisites.sh
cd /opt/intel/openvino/deployment_tools/demo
./demo_squeezenet_download_convert_run.sh
