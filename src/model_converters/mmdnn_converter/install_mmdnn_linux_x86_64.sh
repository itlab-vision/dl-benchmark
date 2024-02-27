#!/bin/bash

# Create virtual environment for MMdnn
conda create -n mmdnn python=3.6

conda activate mmdnn
conda install pip
# Install requirements to the virtual environment
pip install -r requirements.txt
conda deactivate
