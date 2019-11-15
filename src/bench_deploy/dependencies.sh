yes | sudo apt install python3-pip3
yes | sudo apt install python3-venv

cd ~/Documents
mkdir benchmark
cd benchmark
rm -rf OpenVINO_env
python3 -m venv OpenVINO_env
source OpenVINO_env/bin/activate

yes | pip3 install PyYAML