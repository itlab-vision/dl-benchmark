#!/bin/bash

# Создание виртуального окружения openvino
conda create -n openvino
conda activate openvino
sudo apt install python3-pip

pip install openvino-dev
export PATH=$PATH:/home/user/.local/bin

# Создание виртуального окружения mmdnn
conda create -n mmdnn python=3.6
conda activate mmdnn
sudo apt install python3-pip

pip install -r requirements.txt
