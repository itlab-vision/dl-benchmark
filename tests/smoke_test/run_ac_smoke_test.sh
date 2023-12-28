#!/bin/bash

. ./utils.sh

omz_downloader --output_dir working_dir_smoke --cache_dir cache_dir_smoke      --name=Sphereface
omz_converter  --output_dir working_dir_smoke --download_dir working_dir_smoke --name=Sphereface --precisions FP32

# prepare reduced LFW dataset (only people with name starting with A)
root_folder="$PWD"
[ -f lfw.pickle ] && rm lfw.pickle
mkdir -p datasets_smoke/LFW && cd datasets_smoke/LFW
if [[ ! -d lfw ]]
then
    [[ ! -f lfw-a.tgz ]] && wget http://vis-www.cs.umass.edu/lfw/lfw-a.tgz
    tar -xf lfw-a.tgz
fi
mkdir -p annotation && cd annotation
wget http://vis-www.cs.umass.edu/lfw/pairs.txt -O pairs.txt.bak
grep -E '^A[[:graph:]]+[[:space:]][[:digit:]]+[[:space:]][[:digit:]]+' pairs.txt.bak > pairs.txt
wget https://raw.githubusercontent.com/clcarwin/sphereface_pytorch/master/data/lfw_landmark.txt -O lfw_landmark.txt.bak
grep ^A lfw_landmark.txt.bak > lfw_landmark.txt
cd "$root_folder"

result_file="results_accuracy.csv"
[ -f $result_file ] && rm $result_file

python3 ../../src/accuracy_checker/accuracy_checker.py -c smoke_config_accuracy.xml -s datasets_smoke/ -r $result_file -d "$(python3 -c "import openvino.model_zoo as omz; print(omz.__path__[0])")"/data/dataset_definitions.yml
check_exit_code accuracy_checker
check_results_file $result_file 1

exit $return_value