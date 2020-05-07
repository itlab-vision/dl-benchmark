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

## Repo Structure

- `docs` directory contains project documentation.
  - [`concept.md`](docs/concept.md) is a concept description
    (goals and tasks).
  - [`technologies.md`](docs/technologies.md) is a list
    of technologies.
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
  - `bench_deploy` is a set of tools for deployment.
  - `benchmark` is a set of scripts to estimate inference
    performance of different models at the single local computer.
  - `configs` contains template configuration files.
  - `csv2html` is a set of scripts to convert result table
    from csv format to html format.
  - `inference` contains inference implementation.
  - `remote_control` contains scripts to execute benchmark
    remotely.

## System Deployment
In order to deploy the benchmark system, you must perform the following
sequence of actions:
1. Select the required Dockerfile from the `docker` folder.
2. Update all the variables in the file, the necessary
  variables are marked as `ARGS`.
3. The next step is to build the image, the instruction is
  presented in `docker/README.md`
4. It is necessary to prepare the FTP-server in advance,
  and also create a folder on it where docker images will be uploaded.
5. You must fill in the `src/configs/deploy_configuration_file_template.xml`
  configuration file according to the instructions.
6. Next, you need to run `src/deployment/deploy.py`, the instructions for
  starting are in the same folder.
7. The last step is to copy the test data set to the image, using the
  command: `docker cp <PathToData> <ContainerName>:/tmp/data`.

## System Startup
In order to start the system, it is necessary to create two new folders
on the already created FTP-server, one for the benchmark configuration files,
and the second for the work results.
To start testing, you must perform the following steps:
1. Prepare configuration files, `src/configs/benchmark_configuration_file_template.xml`
  and `src/configs/remote_configuration_file_template.xml` will be necessary.
2. Place the benchmark configuration files in a folder on the FTP-server.
3. Run the `src/remote_control/remote_start.py` script, the instructions
  for starting are located in the same folder.
4. Wait for the tests to complete.
5. Take the results from the FTP-server.

<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[dli-ru-web-page]: http://hpc-education.unn.ru/dli-ru
[dli-web-page]: http://hpc-education.unn.ru/dli
[open-model-zoo]: https://github.com/opencv/open_model_zoo
