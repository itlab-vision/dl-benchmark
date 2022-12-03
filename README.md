# DLI: Deep Learning Inference Benchmark

## Introduction

This is a repo of deep learning inference benchmark, called DLI.
DLI is a benchmark for deep learning inference on various hardware.
The main advantage of DLI from the existing benchmarks
is the availability of performance results for a large number
of deep models inferred on Intel platforms (Intel CPUs, Intel
Processor Graphics, Intel Movidius Neural Compute Stick).

DLI supports: 
- [Intel® Distribution of OpenVINO™ Toolkit][openvino-toolkit].
- [Intel® Optimization for Caffe][intel-caffe].
- [Intel® Optimization for TensorFlow][intel-tensorflow].

More information about DLI is available
[here][dli-ru-web-page] (in Russian)
or [here][dli-web-page] (in English).

## License

This project is licensed under the terms of the [Apache 2.0 license](LICENSE).

## Cite

Please consider citing the following papers.

1. Kustikova V., Vasilyev E., Khvatov A., Kumbrasiev P., Rybkin R.,
Kogteva N. DLI: Deep Learning Inference Benchmark //
Communications in Computer and Information Science.
V.1129. 2019. P. 542-553.

1. Sidorova A.K.,  Alibekov M.R., Makarov A.A., Vasiliev E.P., 
Kustikova V.D. Automation of collecting performance indicators 
for the inference of deep neural networks in Deep Learning 
Inference Benchmark // Mathematical modeling and supercomputer 
technologies. Proceedings of the XXI International Conference 
(N. Novgorod, November 22–26, 2021). – Nizhny Novgorod: Nizhny
Novgorod State University Publishing House, 2021. – 423 p.
[https://hpc-education.unn.ru/files/conference_hpc/2021/MMST2021_Proceedings.pdf][mmst-2021].
(In Russian)

## Repo structure

- `docker` directory contains Dockerfiles.

  - `OpenVINO_DLDT` is a directory of Dockerfiles for Intel® 
    Distribution of OpenVINO™ Toolkit.
  - `Caffe`is a directory of Dockerfiles for Intel® Optimization 
    for Caffe.
  - `TensorFlow`is a directory of Dockerfiles for Intel® Optimization
    for TensorFlow.

- `docs` directory contains auxiliary documentation. Please, find documentation
  at the [Wiki page][dli-wiki].

- `results` directory contains benchmarking and validation results.

  - [`benchmarking`](results/benchmarking) contains benchmarking 
    results in html and xslx formats.
  - [`accuracy`](results/accuracy) contains accuracy
    results in html and xslx formats.
  - [`validation`](results/validation) contains tables that confirms 
    correctness of inference implemenration.

    - [`validation_results.md`](results/validation/validation_results.md) 
      is a table that confirms correctness of inference implementation 
      based on Intel Distribution of OpenVINO™ toolkit for public models.
    - [`validation_results_intel_models.md`](results/validation/validation_results_intel_models.md)
      is a table that confirms correctness of inference implementation 
      based on Intel® Distribution of OpenVINO™ toolkit for models trained
      by Intel engineers and available in [Open Model Zoo][open-model-zoo].
    - [`validation_results_caffe.md`](results/validation/validation_results.md) 
      is a table that confirms correctness of inference implementation 
      based on Intel® Optimization for Caffe for several public models.
    - [`validation_results_tensorflow.md`](results/validation/validation_results.md) 
      is a table that confirms correctness of inference implementation 
      based on Intel® Optimization for TensorFlow for several public models.

  - [`models_checklist.md`](results/models_checklist.md) contains a list
    of supported deep models (in accordance with the Open Model Zoo).

- `src` directory contains benchmark sources.

  - `accuracy_checker` contains scripts to check deep model accuracy
    using Accuracy Checker of Intel® Distribution of OpenVINO™ toolkit.
  - `benchmark` is a set of scripts to estimate inference
    performance of different models at the single local computer.
  - `config_maker`contains GUI application to make configuration files
    of the benchmark components.
  - `configs` contains template configuration files.
  - `csv2html` is a set of scripts to convert result table
    from csv to html.
  - `csv2xlsx` is a set of scripts to convert result table
    from csv to xlsx.
  - `deployment` is a set of deployment tools.
  - `inference` contains inference implementation.
  - `node_info` contains a set of functions to get information about
    computational node.
  - `onnxruntime_benchmark` is the tool that allows to measure
    deep learning models inference performance with
    [ONNX Runtime](https://github.com/microsoft/onnxruntime).
    This implementation inspired by [OpenVINO Benchmark C++ tool](https://github.com/openvinotoolkit/openvino/tree/master/samples/cpp/benchmark_app)
    as a reference and stick to its measurement methodology,
    thus provide consistent performance results.
  - `quantization` contains scripts to quantize model to INT8-precision
    using Post-Training Optimization Tool (POT) of Intel® Distribution of OpenVINO™ toolkit.
  - `remote_control` contains scripts to execute benchmark
    remotely.
  - `utils` is a package of auxiliary utilities.

# Documentation

Please, follow project [wiki][dli-wiki].


<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[intel-caffe]: https://github.com/intel/caffe
[intel-tensorflow]: https://www.intel.com/content/www/us/en/developer/articles/guide/optimization-for-tensorflow-installation-guide.html
[dli-ru-web-page]: http://hpc-education.unn.ru/dli-ru
[dli-web-page]: http://hpc-education.unn.ru/dli
[open-model-zoo]: https://github.com/opencv/open_model_zoo
[mmst-2021]: https://hpc-education.unn.ru/files/conference_hpc/2021/MMST2021_Proceedings.pdf
[dli-wiki]: https://github.com/itlab-vision/dl-benchmark/wiki
