#!/bin/bash

password=$1

echo $password | sudo -S yes | apt install python3-pip3
sudo apt-get install python3-venv

cd ~/Documents
mkdir benchmark
cd benchmark
sudo -S rm -rf OpenVINO_env
sudo python3 -m venv OpenVINO_env
source OpenVINO_env/bin/activate

sudo pip3 install PyYAML
sudo pip3 install requests
sudo pip3 install numpy
sudo pip3 install networkx==2.3
sudo pip3 install defusedxml
sudo pip install protobuf==3.6.1