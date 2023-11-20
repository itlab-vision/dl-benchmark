#!/bin/bash

# Создание виртуального окружения mmdnn
conda create -n mmdnn1 python=3.6
conda activate mmdnn1
conda install pip

pip install -r requirements.txt
conda deactivate