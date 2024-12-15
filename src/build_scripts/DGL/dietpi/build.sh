#!/bin/bash

echo "Install PyTorch"

pip install torch==2.2.1
pip install torchaudio==2.2.1
pip install torchvision==0.17.1

echo "Install gcc"

sudo apt-get install gcc

echo "Install DGL"

pip install dgl==2.0.0 -f https://data.dgl.ai/wheels/repo.html
pip install dglgo==0.0.2 -f https://data.dgl.ai/wheels-test/repo.html

echo "Installation completed successfully"