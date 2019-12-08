#!/bin/bash

password=$1

echo $password | sudo -S yes | apt install python3-pip3
echo $password | sudo -S yes | apt-get install python3-venv

cd ~/Documents
mkdir benchmark
cd benchmark
echo $password | sudo -S yes | rm -rf OpenVINO_env
echo $password | sudo -S yes | python3 -m venv OpenVINO_env
source OpenVINO_env/bin/activate

echo $password | sudo -S yes | sudo pip3 install PyYAML
echo $password | sudo -S yes | sudo pip3 install requests
echo $password | sudo -S yes | sudo pip3 install numpy
echo $password | sudo -S yes | sudo pip3 install networkx==2.3
echo $password | sudo -S yes | sudo pip3 install defusedxml
echo $password | sudo -S yes | sudo pip install protobuf==3.6.1