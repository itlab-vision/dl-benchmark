#!/bin/bash

dowload_link=$1
password=$2

#Installation status
status=0

echo "Update components"
yes | apt-get update

echo "Delete old components"
echo $password | sudo -S rm -rf /home/itmm/inference_engine_samples_build
echo $password | sudo -S rm -rf /home/itmm/openvino_models

echo "Install python dependencies"
echo $password | sudo -S ./dependencies.sh $password

source ~/Documents/benchmark/OpenVINO_env/bin/activate

cd ~/Downloads/
wget $dowload_link

arch_name="$(ls | grep ".tgz")"
tar -xvzf $arch_name
cd "$(basename $arch_name .tgz)"
sed -i 's/=decline/=accept/' silent.cfg

echo "Delete old openvino"
sed -i 's/=install/=uninstall/' silent.cfg
echo $password | sudo -S ./install.sh --silent silent.cfg

echo "Install new openvino"
sed -i 's/=uninstall/=install/' silent.cfg
echo $password | sudo -S ./install.sh --silent silent.cfg
if [ $status -eq 0 ]; then status=$? fi

echo "Install openvino dependencies"
cd /opt/intel/openvino/install_dependencies
echo $password | sudo -S ./install_openvino_dependencies.sh -E
if [ $status -eq 0 ]; then status=$? fi

echo "Setting vars"
source /opt/intel/openvino/bin/setupvars.sh

echo "Configurate model_optimizer"
cd /opt/intel/openvino/deployment_tools/model_optimizer/install_prerequisites
echo $password | sudo -S ./install_prerequisites.sh
if [ $status -eq 0 ]; then status=$? fi

echo "Test run"
cd /opt/intel/openvino/deployment_tools/demo
./demo_squeezenet_download_convert_run.sh
if [ $status -eq 0 ]; then status=$? fi

# cd /opt/intel/openvino/deployment_tools/open_model_zoo/tools/downloader
# source ~/Documents/benchmark/OpenVINO_env/bin/activate

# python3 -mpip install --user -r ./requirements.in

# echo "Download models"
# sudo ./downloader.py --all
# if [ $status -eq 0 ]; then status=$? fi

# echo "Setting vars"
# source /opt/intel/openvino/bin/setupvars.sh

# echo "Convert to FP16"
# sudo ./converter.py --all --precisions=FP16 --mo ../../../model_optimizer/mo.py
# if [ $status -eq 0 ]; then status=$? fi
# echo "Convert to FP32"
# sudo ./converter.py --all --precisions=FP32 --mo ../../../model_optimizer/mo.py
# if [ $status -eq 0 ]; then status=$? fi
# echo "Convert to INT8"
# sudo ./converter.py --all --precisions=INT8 --mo ../../../model_optimizer/mo.py
# if [ $status -eq 0 ]; then status=$? fi

if [ $status -eq 0 ]; then echo "InstallSuccess" fi
