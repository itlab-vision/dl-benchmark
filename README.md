# DLI: Deep Learning Inference Benchmark based on Intel® Distribution of OpenVINO™ toolkit

## Introduction

This is a repo of deep learning inference benchmark, called DLI.
DLI is a benchmark for deep learning inference on various hardware.
The main advantage of DLI from the existing benchmarks
is the availability of perfomance results for a large number
of deep models inferred on Intel platforms (Intel CPUs, Intel
Processor Graphics, Intel Movidius Neural Compute Stick).
DLI is based on the [Intel® Distribution of OpenVINO™ toolkit][openvino-toolkit].

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

- `results` directory contains validation results.
  - [`validation_results.md`](results/validation_results.md) is a table
    that confirms correctness of inference implementation based on
    Intel® Distribution of OpenVINO™ toolkit for public models.
  - [`validation_results_intel_models.md`](results/validation_results_intel_models.md)
    is a table that confirms correctness of inference implementation based on
    Intel® Distribution of OpenVINO™ toolkit for models trained
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

<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[dli-ru-web-page]: http://hpc-education.unn.ru/dli-ru
[dli-web-page]: http://hpc-education.unn.ru/dli
[open-model-zoo]: https://github.com/opencv/open_model_zoo
