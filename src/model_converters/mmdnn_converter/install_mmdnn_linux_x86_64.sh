#!/bin/bash

# Создание виртуального окружения mmdnn
conda create -n mmdnn python=3.6
conda activate mmdnn
conda install pip

pip install -r requirements.txt
conda deactivate
