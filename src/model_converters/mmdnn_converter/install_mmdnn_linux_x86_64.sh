#!/bin/bash -x


# Обновление системы
sudo apt update && sudo apt upgrade -y


# Создание виртуального окружения openvino
conda create -n openvino
conda activate openvino

# Установка openvino
pip install openvino openvino-dev
export PATH=$PATH:/home/user/.local/bin

# Создание виртуального окружения mmdnn
conda create -n mmdnn python=3.6
conda activate mmdnn
sudo apt-get install python3-pip

pip install six==1.14.0
pip install setuptools==46.1.3
pip install wget==3.2 2>/tmp/wget.err
if [ $? != 0 ];then
   pth_file=$(cat /tmp/wget.err | grep '.pth' | head -n 1 | tr ' ' '\n' | grep pth | tr -d ':')
   rm -fv $pth_file
   pip uninstall wget
   pip install wget==3.2 2> /tmp/wget.err2
fi
pip install numpy==1.18.2 2>/tmp/numpy.err
if [ $? != 0 ];then
   pth_file=$(cat /tmp/numpy.err | grep '.pth' | head -n 1 | tr ' ' '\n' | grep pth | tr -d ':')
   rm -fv $pth_file
   pip uninstall numpy
   pip install numpy==1.18.2 2> /tmp/numpy.err2
fi

pip install scipy==1.4.1 2>/tmp/scipy.err
if [ $? != 0 ];then
   pth_file=$(cat /tmp/scipy.err | grep '.pth' | head -n 1 | tr ' ' '\n' | grep pth | tr -d ':')
   rm -fv $pth_file
   pip uninstall scipy
   pip install scipy==1.4.1 2> /tmp/scipy.err2
fi
pip install scikit-image==0.16.2
pip install protobuf==3.11.3
pip install pillow==6.2.2
pip install tensorflow==1.15.2
pip install keras==2.2.4
pip install coremltools==2.1.0
pip install h5py==2.7.1
pip install torch==1.5.1
pip install torchvision==0.2.1
pip install onnx==1.4.1
pip install onnx-tf==1.2.1
pip install mmdnn
