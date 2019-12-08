yes | sudo apt install python3-pip3
yes | sudo apt-get install python3-venv

cd ~/Documents
mkdir benchmark
cd benchmark
rm -rf OpenVINO_env
python3 -m venv OpenVINO_env
source OpenVINO_env/bin/activate

yes | pip3 install PyYAML
yes | pip3 install requests
yes | pip3 install numpy
yes | pip3 install networkx==2.3
yes | pip3 install defusedxml
yes | pip install protobuf==3.6.1