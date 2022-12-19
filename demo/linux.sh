#!/bin/bash

while getopts l:p:d: flag
do
    case "${flag}" in
        l) login=${OPTARG};;
        p) password=${OPTARG};;
        d) benchmark_datasets=${OPTARG};;
    esac
done


echo "[ INFO ] Demo application has been started"
demo_folder="$PWD"
root_folder="${demo_folder}/.."
openvino_version="2022.1.0"


echo "[ INFO ] System environment creation has been started"
venv_path="${demo_folder}/.venv"
[ -d $venv_path ] && rm -rf $venv_path
python3 -m venv .venv
PYTHON="${venv_path}/bin/python3"
$PYTHON -m pip install -r $root_folder/requirements.txt
echo "[ INFO ] Python environment ${python3} has been created"
sudo apt-get install -y python3-tk docker.io
echo "[ INFO ] Packages python3-tk, docker.io have been installed"
echo "[ INFO ] System environment creation has been completed"


echo "[ INFO ] Creation server has been started"
server_folder="${demo_folder}/server"
[ -d $server_folder ] && rm -rf $server_folder
mkdir $server_folder && cd $server_folder
echo "[ INFO ] Cloning of DLI Benchmark repository"
dlb_server="${server_folder}/dl-benchmark"
git clone https://github.com/itlab-vision/dl-benchmark.git
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
git clone https://github.com/itlab-vision/dl-benchmark.git
echo "[ INFO ] Cloning of OMZ repository"
omz_client="${client_folder}/open_model_zoo"
[ -d $omz_client ] && rm -rf $omz_client
git clone https://github.com/openvinotoolkit/open_model_zoo.git --recursive --branch $openvino_version --single-branch
models_dir="${omz_client}/tools/accuracy_checker/data/test_models"
echo "[ INFO ] Downloading of dataset 'cifar-10-python'"
wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
mkdir dataset && tar xvf cifar-10-python.tar.gz -C dataset
datasets_dir="${client_folder}/datasets"
rm -rf cifar-10-python.tar.gz
echo "[ INFO ] Creation of client has been been completed"


echo "[ INFO ] Creation of Docker image has been started"
cd $root_folder/docker/OpenVINO_DLDT
image_name="openvino_${openvino_version}"
docker build -t $image_name --build-arg DATASET_DOWNLOAD_LINK=$benchmark_datasets .
echo "[ INFO ] Creation of archive with Docker image"
archive_name="openvino_${openvino_version}.tar"
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
$PYTHON deploy.py -s $ip_address -l $login -p itmm \
                     -i $archive_path \
                     -d $server_folder \
                     -n OpenVINO_DLDT \
                     --machine_list $deployment_config \
                     --project_folder $dlb_client
echo "[ INFO ] Deployment of DLI Benchmark system has been completed"


echo "[ INFO ] Preparing configuration for benchmarking"
cd $demo_folder
benchmark_config="benchmark_config.xml"
benchmark_config_path="${PWD}/${benchmark_config}"
[ -f $benchmark_config_path ] && rm -rf $benchmark_config_path
task="test"
model_name="SampleNet"
model_xml="/media/models/SampLeNet.xml"
model_bin="/media/models/SampLeNet.bin"
framework="OpenVINO DLDT"
device="CPU"
echo \
"<?xml version=\"1.0\" encoding=\"utf-8\"?>
<Tests>
	<Test>
		<Model>
			<Task>${task}</Task>
			<Name>${model_name}</Name>
			<Precision>FP32</Precision>
			<SourceFramework>Caffe</SourceFramework>
			<ModelPath>${model_xml}</ModelPath>
			<WeightsPath>${model_bin}</WeightsPath>
		</Model>
		<Dataset>
			<Name>ImageNET</Name>
			<Path>/tmp/itlab-vision-dl-benchmark-data/Datasets/ImageNET/</Path>
		</Dataset>
		<FrameworkIndependent>
			<InferenceFramework>${framework}</InferenceFramework>
			<BatchSize>1</BatchSize>
			<Device>${device}</Device>
			<IterationCount>10</IterationCount>
			<TestTimeLimit>180</TestTimeLimit>
		</FrameworkIndependent>
		<FrameworkDependent>
			<Mode>sync</Mode>
			<Extension></Extension>
			<AsyncRequestCount></AsyncRequestCount>
			<ThreadCount></ThreadCount>
			<StreamCount></StreamCount>
		</FrameworkDependent>
	</Test>
    <Test>
		<Model>
			<Task>${task}</Task>
			<Name>${model_name}</Name>
			<Precision>FP32</Precision>
			<SourceFramework>Caffe</SourceFramework>
			<ModelPath>${model_xml}</ModelPath>
			<WeightsPath>${model_bin}</WeightsPath>
		</Model>
		<Dataset>
			<Name>ImageNET</Name>
			<Path>/tmp/itlab-vision-dl-benchmark-data/Datasets/ImageNET/</Path>
		</Dataset>
		<FrameworkIndependent>
			<InferenceFramework>${framework}</InferenceFramework>
			<BatchSize>1</BatchSize>
			<Device>${device}</Device>
			<IterationCount>10</IterationCount>
			<TestTimeLimit>180</TestTimeLimit>
		</FrameworkIndependent>
		<FrameworkDependent>
			<Mode>async</Mode>
			<Extension></Extension>
			<AsyncRequestCount></AsyncRequestCount>
			<ThreadCount></ThreadCount>
			<StreamCount></StreamCount>
		</FrameworkDependent>
	</Test>
</Tests>" \
    >> $benchmark_config_path
echo "[ INFO ] Model: ${model_xml}"
echo "[ INFO ] Weights: ${model_bin}"
echo "[ INFO ] Framework: ${framework}"
echo "[ INFO ] Device: ${device}"
echo "[ INFO ] Modes: latency, throughput"
echo "[ INFO ] Copying of benchmark configuration file ${benchmark_config_path} to server"
# use cp instead of scp because scp asks password
[ -f $server_folder/$benchmark_config ] && rm -rf $server_folder/$benchmark_config
cp $benchmark_config_path $server_folder/$benchmark_config
echo "[ INFO ] Preparing of configuration ${benchmark_config_path} has been completed"


echo "[ INFO ] Preparing configuration for accuracy checker"
accuracy_checker_config="accuracy_checker_config.xml"
accuracy_checker_config_path="${PWD}/${accuracy_checker_config}"
[ -f $accuracy_checker_config_path ] && rm -rf $accuracy_checker_config_path
model_path="/media/models"
config_path="${omz_client}/tools/accuracy_checker/sample/sample_config.yml"
echo \
"<?xml version=\"1.0\" encoding=\"utf-8\"?>
<Tests>
	<Test>
		<Model>
			<Task>${task}</Task>
			<Name>${model_name}</Name>
			<Precision>FP32</Precision>
			<SourceFramework>Caffe</SourceFramework>
			<Directory>${model_path}</Directory>
		</Model>
		<Parameters>
			<InferenceFramework>${framework}</InferenceFramework>
			<Device>${device}</Device>
			<Config>${config_path}</Config>
		</Parameters>
	</Test>
</Tests>" \
    >> $accuracy_checker_config_path
echo "[ INFO ] Model: ${model_name}"
echo "[ INFO ] Framework: ${framework}"
echo "[ INFO ] Device: ${device}"
echo "[ INFO ] Config: ${config_path}"
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
sudo apt-get remove -y python3-tk docker.io
cd $demo_folder
echo "[ INFO ] System cleaning has been ended"

echo "[ INFO ] Demo application has been eneded"
