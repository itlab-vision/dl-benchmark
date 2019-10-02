# DLI: Deep Learning Inference Benchmark based on Intel® Distribution of OpenVINO™ toolkit

Deep learning benchmark based on [Intel® Distribution of OpenVINO™ toolkit][openvino-toolkit].

## Repo Structure

- `docs` directory contains project documentation.
  - [`concept.md`](docs/concept.md) is a concept description
    (goals, tasks and requirements).
  - [`technologies.md`](docs/technologies.md) is a list
    of technologies.
  - [`architecture.md`](docs/architecture.md) is a benchmarking
    system architecture.

- `results` directory contains validation and performance results.
  - [`validation_results.md`](results/validation_results.md) is a table
    that confirms correctness of inference implementation based on
    Intel® Distribution of OpenVINO™ toolkit.

- `src` directory contains benchmark sources.
  - `auxiliary` contains auxiliary scripts for benchmarking
    (to get node information).
  - `benchmark` is a set of scripts to estimate inference
    performance of different models at the single local computer.
  - `configs` contains template configuration files.
  - `converter` is a set of scripts to convert models to the
    intermediate representation using Model Optimizer from
	Intel® Distribution of OpenVINO™ toolkit.
  - `csv2html` is a set of scripts to convert result table
  from csv format to html format.
  - `inference` contains inference implementation based on
    Intel® Distribution of OpenVINO™ toolkit.
  - `remote_control` contains scripts to execute benchmark
    remotely.

<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit