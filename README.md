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
  - `deployment` is a set of tools for deployment.
  - `benchmark` is a set of scripts to estimate inference
    performance of different models at the single local computer.
  - `configs` contains template configuration files.
  - `csv2html` is a set of scripts to convert result table
    from csv format to html format.
  - `inference` contains inference implementation.
  - `remote_control` contains scripts to execute benchmark
    remotely.

## Deployment

To deploy DLI, please, follow instructions.

1. Select the required Dockerfile from the `docker` folder.
1. Update all the variables in the file, the necessary
   variables are marked as `ARGS`.
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

<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[dli-ru-web-page]: http://hpc-education.unn.ru/dli-ru
[dli-web-page]: http://hpc-education.unn.ru/dli
[open-model-zoo]: https://github.com/opencv/open_model_zoo
