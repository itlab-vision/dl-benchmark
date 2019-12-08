#!/bin/bash

yes | sudo apt install python3-pip3
yes | sudo apt-get install python3-venv

cd ~/Documents
mkdir benchmark
cd benchmark
sudo rm -rf OpenVINO_env
sudo python3 -m venv OpenVINO_env
source OpenVINO_env/bin/activate

yes | sudo pip3 install PyYAML
yes | sudo pip3 install requests
yes | sudo pip3 install numpy
yes | sudo pip3 install networkx==2.3
yes | sudo pip3 install defusedxml
yes | sudo pip install protobuf==3.6.1