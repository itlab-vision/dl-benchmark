#!/bin/bash

supported_frameworks="OpenVINO_DLDT TensorFlow TensorFlowLite MXNet ONNXRuntime OpenCV PyTorch TVM"

usage() {
    echo "Usage: $0 [-l LOGIN] [-p PASSWORD] [-f FRAMEWORK] [-d GIT_LINK_TO_DATASET]"
    echo "Options:"
    echo "  -l          Login of the current user."
    echo "  -p          Password of the current user."
    echo "  -f          Framework (supported: $supported_frameworks)."
    echo "  -d          The address to the GitHub repository, which contains datasets for benchmarking."
    echo "              It is required that the Databases/ImageNet/ directory be created"
    echo "              in the repository, which stores at least one image."
}

exit_abnormal() {
    usage
    exit 1
}


while getopts :l:p:d:f: flag;
do
    case "${flag}" in
        l)  login=${OPTARG}
            ;;
        p)  password=${OPTARG}
            ;;
        d)  benchmark_datasets=${OPTARG}
            ;;
        f)  framework=${OPTARG}
            ;;
        :)  echo "Error: -${OPTARG} requires an argument."
            exit_abnormal
      ;;
    esac
done

if [[(-z $login) || (-z $password) || (-z $benchmark_datasets) || (-z $framework)]]; then
    echo "One or more of required parameters is not specified."
    exit_abnormal
fi

if [[ ! " $supported_frameworks " =~ " $framework " ]]; then
    echo "Framework '$framework' is not supported."
    exit_abnormal
fi


echo "[ INFO ] Demo application has been started"
demo_folder="$PWD"
root_folder="${demo_folder}/.."
openvino_version="2024.4.0"


echo "[ INFO ] System environment creation has been started"
venv_path="${demo_folder}/.venv"
[ -d $venv_path ] && rm -rf $venv_path
python3 -m venv .venv
PYTHON="${venv_path}/bin/python3"
$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install -r $root_folder/requirements.txt
echo "[ INFO ] Python environment ${python3} has been created"
declare -A packages
packages=( ["python3-tk"]="1" ["docker.io"]="1" ["containerd"]="1")
for pkg in "${!packages[@]}";
do
    pkg_ok=$(dpkg-query -W -f='${Status}' $pkg 2>/dev/null | grep -c "ok installed")
    packages[$pkg]=$pkg_ok
    if [ $pkg_ok -eq 0 ];
    then
      sudo apt-get install -y $pkg
      echo "[ INFO ] Package $pkg has been installed"
    else
        echo "[ INFO ] Package $pkg has been already installed"
    fi
done
echo "[ INFO ] System environment creation has been completed"


echo "[ INFO ] Creation server has been started"
server_folder="${demo_folder}/server"
[ -d $server_folder ] && rm -rf $server_folder
mkdir $server_folder && cd $server_folder
echo "[ INFO ] Cloning of DLI Benchmark repository"
dlb_server="${server_folder}/dl-benchmark"
git clone https://github.com/itlab-vision/dl-benchmark.git --depth 1
dlb_results="${server_folder}/results"
[ -d $dlb_results ] && rm -rf $dlb_results
mkdir $dlb_results && cd $dlb_results
echo "[ INFO ] Creation server has been completed"


echo "[ INFO ] Creation of client has been started"
client_folder="${demo_folder}/client"
[ -d $client_folder ] && rm -rf $client_folder
mkdir $client_folder
cd $client_folder
echo "[ INFO ] Cloning of DLI Benchmark repository"
dlb_client="${client_folder}/dl-benchmark"
[ -d $dlb_client ] && rm -rf $dlb_client
git clone https://github.com/itlab-vision/dl-benchmark.git --depth 1
echo "[ INFO ] Cloning of OMZ repository"
omz_client="${client_folder}/open_model_zoo"
[ -d $omz_client ] && rm -rf $omz_client
git clone https://github.com/openvinotoolkit/open_model_zoo.git --recursive --branch $openvino_version --single-branch --depth 1

if [ "$framework" = "TVM" ]; then
    $PYTHON -m pip install apache-tvm==0.14.dev264 gluoncv[full] mxnet==1.9.1
    $PYTHON -m pip uninstall -y numpy && $PYTHON -m pip install numpy==1.23.1
    models_dir="${client_folder}/tvm_models"
    [ -d $models_dir ] && rm -rf $models_dir
    mkdir $models_dir
    $PYTHON ${dlb_client}/src/model_converters/tvm_converter/tvm_converter.py \
                    -mn "SampleNet_from_MXNet" -f mxnet -is 1 3 32 32 -b 1 -op "${models_dir}" \
                    -m "${omz_client}/tools/accuracy_checker/data/test_models/samplenet-symbol.json" \
                    -w "${omz_client}/tools/accuracy_checker/data/test_models/samplenet-0000.params"
elif [ "$framework" = "TensorFlowLite" ]; then
    $PYTHON -m pip install -r ${dlb_client}/src/model_converters/tf2tflite/requirements.txt
    models_dir="${client_folder}/tflite_models"
    [ -d $models_dir ] && rm -rf $models_dir
    mkdir $models_dir
    $PYTHON ${dlb_client}/src/model_converters/tf2tflite/tflite_converter.py \
                    --model-path "${omz_client}/tools/accuracy_checker/data/test_models/samplenet_tf2/" \
                    --source-framework tf --input-names input --input-shapes "[1, 32, 32, 3]"
    mv "${omz_client}/tools/accuracy_checker/data/test_models/samplenet_tf2.tflite" $models_dir
else
    models_dir="${omz_client}/tools/accuracy_checker/data/test_models"
fi

echo "[ INFO ] Downloading of dataset 'cifar-10-python'"
wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
mkdir dataset && tar xvf cifar-10-python.tar.gz -C dataset
datasets_dir="${client_folder}/dataset"
rm -rf cifar-10-python.tar.gz
echo "[ INFO ] Creation of client has been been completed"


echo "[ INFO ] Creation of Docker image has been started"
cd $root_folder/docker/
dli_dataset_repo_name=${benchmark_datasets##*/}
dli_dataset_repo_name=${dli_dataset_repo_name%.git}
echo "[ INFO ] The name of repository with datasets is $dli_dataset_repo_name"
echo "[ INFO ] Build a base image has been started"
docker build -t ubuntu_for_dli --build-arg DATASET_DOWNLOAD_LINK=$benchmark_datasets .
echo "[ INFO ] Build a base image has been completed"

cd ./$framework
docker_name=${framework}
if [ "$framework" = "OpenVINO_DLDT" ]; then
    image_name="openvino_${openvino_version}"
else
    if [ "$framework" = "ONNXRuntime" ]; then
        docker_name="ONNX_Runtime_Python"
    elif [ "$framework" = "OpenCV" ]; then
        docker_name="OpenCV_DNN_Python"
    elif [ "$framework" = "PyTorch" ]; then
        docker_name="PyTorch"
    elif [ "$framework" = "TensorFlowLite" ]; then
        docker_name="TensorFlowLite"
    fi
    image_name=${docker_name,,}
fi
echo "[ INFO ] Build a $image_name image has been started"
docker build -t $image_name .
echo "[ INFO ] Build a $image_name image has been completed"

echo "[ INFO ] Creation of archive with Docker image"
archive_name="$image_name.tar"
docker save $image_name -o $archive_name
archive_path="$PWD/$archive_name"
echo "[ INFO ] Archive ${archive_path} has been created"
echo "[ INFO ] Creation of Docker image has been completed"


echo "[ INFO ] Deployment of DLI Benchmark system has been started"
cd $demo_folder
ip_address=$(ip -o route get to 8.8.8.8 | sed -n 's/.*src \([0-9.]\+\).*/\1/p')
echo "[ INFO ] IP-address of the host: ${ip_address}"
echo "[ INFO ] Configuration creation for deployment module"
deployment_config="${PWD}/deploy_config.xml"
[ -f $deployment_config ] && rm -rf $deployment_config
echo \
"<?xml version=\"1.0\" encoding=\"utf-8\" ?>
<Computers>
    <Computer>
        <IP>${ip_address}</IP>
        <Login>${login}</Login>
        <Password>${password}</Password>
        <OS>Linux</OS>
        <DownloadFolder>${client_folder}</DownloadFolder>
        <DatasetFolder>${datasets_dir}</DatasetFolder>
        <ModelFolder>${models_dir}</ModelFolder>
    </Computer>
</Computers>" \
    >> $deployment_config
echo "[ INFO ] Launch deploy.py script"
cd $dlb_server/src/deployment
$PYTHON deploy.py -s $ip_address -l $login -p $password \
                     -i $archive_path \
                     -d $server_folder \
                     -n $docker_name \
                     --machine_list $deployment_config \
                     --project_folder $dlb_client
echo "[ INFO ] Deployment of DLI Benchmark system has been completed"

echo "[ INFO ] Preparing configuration for benchmarking"
cd $demo_folder
benchmark_config="benchmark_config.xml"
benchmark_config_path="${PWD}/${benchmark_config}"
[ -f $benchmark_config_path ] && rm -rf $benchmark_config_path
template_benchmark_config="benchmark_configs/${docker_name}.xml"
echo "[ INFO ] Using template config file ${template_benchmark_config}"
sed "s@{DLI_DATASET_REPO_NAME}@$dli_dataset_repo_name@g" $template_benchmark_config > $benchmark_config_path
echo "[ INFO ] Copying of benchmark configuration file ${benchmark_config_path} to server"
# use cp instead of scp because scp asks password
[ -f $server_folder/$benchmark_config ] && rm -rf $server_folder/$benchmark_config
cp $benchmark_config_path $server_folder/$benchmark_config
echo "[ INFO ] Preparing of configuration ${benchmark_config_path} has been completed"


echo "[ INFO ] Preparing configuration for accuracy checker"
accuracy_checker_config="accuracy_checker_config.xml"
accuracy_checker_config_path="${PWD}/${accuracy_checker_config}"
[ -f $accuracy_checker_config_path ] && rm -rf $accuracy_checker_config_path
config_path="${PWD}/accuracy_checker_configs/${docker_name}.yml"
template_accuracy_checker_config="accuracy_checker_configs/${docker_name}.xml"
echo "[ INFO ] Using template config file ${template_accuracy_checker_config}"
sed "s@{CONFIG_PATH}@$config_path@g" $template_accuracy_checker_config > $accuracy_checker_config_path
echo "[ INFO ] Copying of accuracy checker configuration ${accuracy_checker_config_path} file to server"
# use cp instead of scp because scp asks password
[ -f $server_folder/$accuracy_checker_config ] && rm -rf $server_folder/$accuracy_checker_config
cp $accuracy_checker_config_path $server_folder/$accuracy_checker_config
echo "[ INFO ] Preparing of configuration ${accuracy_checker_config_path} has been completed"


echo "[ INFO ] Preparing configuration file for remote control module"
remote_config="remote_config.xml"
remote_config_path="${PWD}/${remote_config}"
[ -f $remote_config_path ] && rm -rf $remote_config_path
echo \
"<?xml version=\"1.0\" encoding=\"utf-8\" ?>
<Computers>
    <Computer>
        <IP>${ip_address}</IP>
        <Login>${login}</Login>
        <Password>${password}</Password>
        <OS>Linux</OS>
        <FTPClientPath>${dlb_client}/src/remote_control/ftp_client.py</FTPClientPath>
        <Benchmark>
            <Config>${server_folder}/${benchmark_config}</Config>
            <Executor>docker_container</Executor>
            <LogFile>${client_folder}/log_bench.txt</LogFile>
            <ResultFile>${client_folder}/result_bench_table.csv</ResultFile>
        </Benchmark>
        <AccuracyChecker>
            <Config>${server_folder}/${accuracy_checker_config}</Config>
            <Executor>docker_container</Executor>
            <DatasetPath>/media/datasets</DatasetPath>
            <DefinitionPath>${omz_client}/tools/accuracy_checker/dataset_definitions.yml</DefinitionPath>
            <LogFile>${client_folder}/log_ac.txt</LogFile>
            <ResultFile>${client_folder}/result_ac_table.csv</ResultFile>
        </AccuracyChecker>
    </Computer>
</Computers>" \
    >> $remote_config_path
echo "[ INFO ] Copying of remote control configuration ${remote_config_path} file to server"
# use cp instead of scp because scp asks password
cp $remote_config_path $server_folder/$remote_config
echo "[ INFO ] Preparing of configuration ${remote_config_path} has been completed"


echo "[ INFO ] Remote experiment launch has been started"
cd $dlb_server/src/remote_control
benchmark_results="benchmark_results.csv"
accuracy_checker_results="accuracy_checker_results.csv"
$PYTHON remote_start.py -c $server_folder/$remote_config \
                         -s $ip_address -l $login -p $password \
                         -br $benchmark_results \
                         -acr $accuracy_checker_results \
                         --ftp_dir $dlb_results
echo "[ INFO ] The remote experiments has been completed"


echo "[ INFO ] Copying of ${benchmark_results} file to host"
benchmark_results_csv="${demo_folder}/${benchmark_results}"
accuracy_checker_results_csv="${demo_folder}/${accuracy_checker_results}"
cp $dlb_results/$benchmark_results $benchmark_results_csv
echo "[ INFO ] Copying of ${accuracy_checker_results} file to host"
cp $dlb_results/$accuracy_checker_results $accuracy_checker_results_csv


echo "[ INFO ] Creation of xlsx files"
benchmark_results_xlsx="${demo_folder}/benchmark_results.xslx"
accuracy_checker_results_xlsx="${demo_folder}/accuracy_checker_results.xslx"
cd $root_folder/src/csv2xlsx
echo "[ INFO ] XLSX table with benchmarking results has been saved in ${benchmark_results_xlsx}:"
DISPLAY=localhost:0.0 $PYTHON converter.py -k benchmark -t $benchmark_results_csv -r $benchmark_results_xlsx
cat $benchmark_results_xlsx
echo "[ INFO ] XLSX table with accuracy checker results has been saved in ${accuracy_checker_results_xlsx}:"
DISPLAY=localhost:0.0 $PYTHON converter.py -k accuracy_checker -t $accuracy_checker_results_csv -r $accuracy_checker_results_xlsx
cat $accuracy_checker_results_xlsx


echo "[ INFO ] Creation of html files"
benchmark_results_html="${demo_folder}/benchmark_results.html"
accuracy_checker_results_html="${demo_folder}/accuracy_checker_results.html"
cd $root_folder/src/csv2html
$PYTHON converter.py -k benchmark -t $benchmark_results_csv -r $benchmark_results_html
echo "[ INFO ] HTML table with benchmarking results has been saved in ${benchmark_results_html}"
$PYTHON converter.py -k accuracy_checker -t $accuracy_checker_results_csv -r $accuracy_checker_results_html
echo "[ INFO ] HTML table with accuracy checker results has been saved in ${accuracy_checker_results_html}"


echo "[ INFO ] System cleaning has been started"
for pkg in "${!packages[@]}";
do
    echo "$pkg - ${packages[$pkg]}"
    if [ ${packages[$pkg]} -eq 0 ];
    then
      sudo apt-get autoremove --purge -y $pkg
      echo "[ INFO ] The package $pkg has been removed"
    fi
done
cd $demo_folder
echo "[ INFO ] System cleaning has been ended"

echo "[ INFO ] Demo application has been eneded"
