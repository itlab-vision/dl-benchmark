# DLI: Deep Learning Inference Benchmark based on Intel® Distribution of OpenVINO™ Toolkit

## Introduction

This is a repo of deep learning inference benchmark, called DLI.
DLI is a benchmark for deep learning inference on various hardware.
The main advantage of DLI from the existing benchmarks
is the availability of perfomance results for a large number
of deep models inferred on Intel platforms (Intel CPUs, Intel
Processor Graphics, Intel Movidius Neural Compute Stick).
DLI is based on the [Intel® Distribution of OpenVINO™ Toolkit][openvino-toolkit].

More information about DLI is available
[here][dli-ru-web-page] (in Russian)
or [here][dli-web-page] (in English).

## Cite

Please consider citing the following paper.

Kustikova V., Vasilyev E., Khvatov A., Kumbrasiev P., Rybkin R.,
Kogteva N. DLI: Deep Learning Inference Benchmark //
Communications in Computer and Information Science.
V.1129. 2019. P. 542-553.

## Repo structure
- `docker` directory contains Dockerfiles.
  - [`Dockerfile`](docker/Dockerfile) is a file to build the OpenVINO toolkit.

- `docs` directory contains project documentation.
  - [`concept.md`](docs/concept.md) is a concept description
    (goals and tasks).
  - [`technologies.md`](docs/technologies.md) is a list of technologies.
  - [`architecture.md`](docs/architecture.md) is a benchmarking
    system architecture.

- `results` directory contains benchmarking and validation results.
  - [`benchmarking`](results/benchmarking) contains benchmarking 
    results in html format.
  - [`validation`](results/validation) contains tables that confirms 
    correctness of inference implemenration.
    - [`validation_results.md`](results/validation/validation_results.md) 
      is a table that confirms correctness of inference implementation 
      based on Intel Distribution of OpenVINO toolkit for public models.
    - [`validation_results_intel_models.md`](results/validation/validation_results_intel_models.md)
      is a table that confirms correctness of inference implementation 
      based on Intel Distribution of OpenVINO toolkit for models trained
      by Intel engineers and available in [Open Model Zoo][open-model-zoo].

- `src` directory contains benchmark sources.
  - `deployment` is a set of deployment tools.
  - `benchmark` is a set of scripts to estimate inference
    performance of different models at the single local computer.
  - `configs` contains template configuration files.
  - `csv2html` is a set of scripts to convert result table
    from csv to html.
  - `inference` contains inference implementation.
  - `remote_control` contains scripts to execute benchmark
    remotely.

## Deployment

To deploy DLI, please, follow instructions.

1. Select the required Dockerfile from the `docker` folder.
1. Update all the variables in the file, the necessary
   variables are marked as `ARG`.
1. The following step is to build the image in accordance with
   `docker/README.md`
1. It is required to deploy FTP-server in advance,
   and create a directory for storing docker images.
1. Create deployment configuration file according to
   the `src/configs/deploy_configuration_file_template.xml`.
1. Execute `src/deployment/deploy.py` in accordance with `src/deployment/README.md`.
1. Copy the test datasets to the docker image, using the following
   command line: `docker cp <PathToData> <ContainerName>:/tmp/data`.

## Startup

To start benchmarking, it is required to create two new directories
on the FTP-server, the first one for the benchmark configuration files,
and the second one for the file of bencmarking results. Further, please,
follow instructions.

1. Prepare configuration files (in accordance with
   `src/configs/benchmark_configuration_file_template.xml` and
   `src/configs/remote_configuration_file_template.xml`.
1. Copy the benchmark configuration files to the corresponding directory
   on the FTP-server.
1. Execute the `src/remote_control/remote_start.py` script. Please, follow
   `src/remote_control/README.md`.
1. Wait for completing the benchmark.
1. Copy benchmarking results from the FTP-server to the local machine.

## Deployment example

1. Download deep learning inference benchmark. Clone repo to the `/tmp`
   directory using the following commands:

   ```bash
   cd tmp
   git clone https://github.com/itlab-vision/openvino-dl-benchmark.git
   ```

1. It is required to deploy FTP-server and create directories.
   For definiteness, we will use the following directory names:

   - `docker_image_folder` is a directory for storing docker image.
   - `benchmark_config` is a directory for storing configurationn files.
   - `table_folder` is a directory for storing performance results.

1. For definiteness, we select the OpenVINO Docker container. The Dockerfile
   to build this image can be found in the
   `/tmp/openvino-dl-benchmark/docker/OpenVINO_DLDT` folder.
   Before building, you should put the current link to download
   the OpenVINO toolkit. Please, insert correct path in the following line:

   `ARG DOWNLOAD_LINK=<Link to download Intel Distribution of OpenVINO Toolkit>`

1. To build docker image, please, use the following command:

   `docker build -t OpenVINO_Image . `

   The `build` option searches for the Dockerfile in the current directory
   and builds the image `OpenVINO_Image`.

1. The following step is to add docker-image to the archive by the command:

   `docker save OpenVINO_Image > OpenVINO_Image.tar`

1. After building the image, you need to fill out the configuration file for
   the system deployment script. The configuration file template is located
   in the `/tmp/openvino-dl-benchmark/src/config/deploy_configuration_file_template.xml`.
   Fill the configuration file (information to access to the remote computer)
   and save it to the `/tmp/openvino-dl-benchmark/src/deployment/deploy_config.xml`.

   ```xml
   <Computers>
     <Computer>
       <IP>4.4.4.4</IP>
       <Login>admin</Login>
       <Password>admin</Password>
       <OS>Linux</OS>
       <DownloadFolder>/tmp/docker_folder</DownloadFolder>
     </Computer>
   </Computers>
   ```
1. To run the deployment script, use the following command: 

   ```bash
   python3 deploy.py -s 2.2.2.2 -l admin -p admin \
       -i /tmp/openvino-dl-benchmark/docker/OpenVINO_Image.tar \
       -d docker_image_folder -n OpenVINO_DLDT \
       --machine_list /tmp/openvino-dl-benchmark/src/deployment/deploy_config.xml \
       --project_folder /tmp/openvino-dl-benchmark/
    ```

   After this stage, there is a docker container at each computer.

1. It is required to copy the datasets for inference using the following command:

   `docker cp /tmp/data/ImageNet OpenVINO_DLDT:/tmp/data/`

## Startup example

1. Fill out the configuration file for the benchmarking script. It is required
   to describe tests to be performed, you can find the template in the
   `src/config/benchmark_configuration_file_template.xml`.
   Fill it and save on `/benchmark_config/bench_config.xml`.

   ```xml
   <Tests>
     <Test>
       <Model>
           <Task>Classification</Task>
           <Name>densenet-121</Name>
           <Precision>FP32</Precision>
           <SourceFramework>Caffe</SourceFramework>
           <Path>/opt/intel/openvino/deployment_tools/tools/model_downloader/public/densenet-121/FP32</Path>
       </Model>
       <Dataset>
           <Name>ImageNet</Name>
           <Path>/tmp/data/</Path>
       </Dataset>
       <FrameworkIndependent>
           <InferenceFramework>OpenVINO_DLDT</InferenceFramework>
           <BatchSize>2</BatchSize>
           <Device>CPU</Device>
           <IterationCount>10</IterationCount>
           <TestTimeLimit>1000</TestTimeLimit>
       </FrameworkIndependent>
       <FrameworkDependent>
           <Mode>Sync</Mode>
           <Extension></Extension>
           <AsyncRequestCount></AsyncRequestCount>
           <ThreadCount></ThreadCount>
           <StreamCount></StreamCount>
       </FrameworkDependent>
     </Test>
   </Tests>
   ```

1. Fill out the configuration file for the
   remote start script, you can find the template in the
   `src/config/remote_configuration_file_template.xml`.
   Fill it and save to the
   `/tmp/openvino-dl-benchmark/src/remote_start/remote_config.xml`.

   ```xml
   <Computers>
     <Computer>
       <IP>4.4.4.4</IP>
       <Login>admin</Login>
       <Password>admin</Password>
       <OS>Linux</OS>
       <FTPClientPath>/tmp/openvino-dl-benchmark/src/remote_start/ftp_client.py</FTPClientPath>
       <OpenVINOEnvironmentPath>/opt/intel/openvino/deployment_tools/bin/setupvars.sh</OpenVINOEnvironmentPath>
       <BenchmarkConfig>/benchmark_config/bench_config.xml</BenchmarkConfig>
       <LogFile>/tmp/openvino-dl-benchmark/src/remote_start/log.txt</LogFile>
       <ResultFile>/tmp/openvino-dl-benchmark/src/remote_start/result.csv</ResultFile>
     </Computer>
   </Computers>
   ```

1. Execute the remote start script using the following command:

   ```bash
   python3 remote_start \
   -c /tmp/openvino-dl-benchmark/src/remote_start/remote_config.xml \
   -s 2.2.2.2 -l admin -p admin -r /table_folder/all_results.csv
   ```

1. Wait for completing the benchmark. After completion,
   the `table_folder` directory will contain a table with the combined results
   named `all_results`.

1. Copy benchmarking results from the FTP-server to the local machine.

   `scp admin@2.2.2.2:/table_folder/all_results.csv /tmp/`

1. Convert the results to html using the following command:

   ```bash
   python -t /tmp/all_results.csv -r /tmp/formatted_results.html
   ```


<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[dli-ru-web-page]: http://hpc-education.unn.ru/dli-ru
[dli-web-page]: http://hpc-education.unn.ru/dli
[open-model-zoo]: https://github.com/opencv/open_model_zoo
