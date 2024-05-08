# Measuring the inference performance of deep neural networks

## Description of inference_benchmark.py

### Basic information

The script allows you to measure the inference performance
of deep models using different frameworks. Currently we support
the following frameworks:

- [Intel® Distribution of OpenVINO™ Toolkit][openvino-toolkit]
  (C++ and Python APIs).
- [Intel® Optimization for Caffe][intel-caffe] (Python API).
- [Intel® Optimizations for TensorFlow][intel-tensorflow] (Python API).
- [TensorFlow Lite][tensorflow-lite] (C++ and Python APIs).
- [ONNX Runtime][onnx-runtime] (C++ and Python APIs).
- [MXNet][mxnet] (Python Gluon API).
- [OpenCV DNN][opencv] (C++ and Python APIs).
- [PyTorch][pytorch] (C++ and Python APIs).
- [Deep Graph Library][dgl-pytorch] (PyTorch-based).
- [Apache TVM][tvm] (Python API).
- [RKNN][rknn].
- [Spektral][spektral] (Python API).

### Implemented algorithm

The benchmark script accepts test configurations as input. Description
of the test configuration can be found [here](../configs/README.md).

The test is inference of one model with the parameters passed
in the configuration file.

The tests are carried out sequentially. Each test is esecuted in
a separate process.

### Script results

The test results are inference performance metrics for the parameters
passed in the configuration file. The results are written to the file,
represented by a csv-table.

## Performance metrics

### Metrics for the Intel® Distribution of OpenVINO™ Toolkit

The software is verified using the Inference Engine component
of the Intel® Distribution of OpenVINO™ Toolkit. The OpenVINO toolkit
provides two inference modes.

1. **Latency mode**.This mode involves creating and executing
   a single request to infer the model on the selected device.
   The next inference request is created after completing
   of the previous one. During performance analysis, the number
   of requests is determined by the iterations number of the test
   loop. Latency mode minimizes inference time of the single request.
1. **Throughtput mode**. It involves creating a set of requests
   to infer the neural network on the selected device. The order
   of requests completion is an arbitrary one. The number of requests
   sets is determined by the number of iterations of the test loop.
   Throughput mode minimizes inference time of the overal requests set.

Inference Engine provides two programming interfaces.

1. **Sync API** is used to implement latency mode.
1. **Async API** is used to implement latency mode if a single request
   is created, and throughput mode, otherwise.

A single inference request corresponds to the feed forward
of the neural network for a batch of images. Required test parameters:

- batch size,
- number of iterations (the number of time taken to infer one request
  for the latency mode and a set of requests for the througput mode),
- number of requests created in throughput mode.

Inference can be executed in multi-threading mode. The number
of threads is an inference parameter (by default, it equals
the number of phisycal cores).

For throughput mode there is a possibility to execute requests
in parallel using streams. Stream is a group of physical threads.
The number of streams is a parameter too. By default number of streams
equals number of requests.

Due to the fact that the OpenVINO toolkit provides two inference modes,
performance measurements are taken for each mode. Evaluating inference
performance for **the latency mode**, requests are executed sequentially.
The next request is infered after the completion of the previous one.
For each request, its duration time is measured. The standard deviation
is calculated on the set of obtained durations and the ones that goes
beyond three standard deviations relative to the mean inference time
are discarded. The final set of times is used to calculate the performance
metrics for the latency mode.

- **Latency** is a median of execution times.
- **Average time of a single pass** is the ratio of the total execution
  time of all iterations to the number of iterations.
- **Batch frames per second, Batch FPS** is the ratio of the batch size
  to the latency.
- **Frames per second, FPS** is the ratio of the total number of processed
  images to the total execution time.

For **the throughput mode**, performance metrics are provided below.

- **Average time of a single pass** is the ratio of the execution time
  of all requests sets to the iterations number of the test loop.
  It is the execution time of a set of simultaneously created requests
  on the device.
- **Batch frames per second, Batch FPS** is the ratio of the product
  of the batch size and the iterations number to the execution time
  of all requests.
- **Frames per second, FPS** is the ratio of the total number
  of processed images to the total execution time.

**Note:** published tables contain only FPS indicators (until 06.2023
the table contained Batch FPS indicators).

### Metrics for Intel® Optimization for Caffe, Intel® Optimizations for TensorFlow, TensorFlow Lite, OpenCV, MXNet, PyTorch and ONNX Runtime

Inference performance evaluations for Intel® Optimization for Caffe,
Intel® Optimizations for TensorFlow, TensorFlow Lite, OpenCV, MXNet,
PyTorch, and ONNX Runtime run queries sequentially and independently.
The next request is infered after the completion of the previous one.
For each request, its duration time is measured. The standard deviation
is calculated on the set of obtained durations and the ones that goes
beyond three standard deviations relative to the mean inference time
are discarded. The final set of times is used to calculate the performance
metrics.

- **Latency** is a median of execution times.
- **Average time of a single pass** is the ratio of the total execution
  time of all iterations to the number of iterations.
- **Batch frames per second, BATCH FPS** is the ratio of the batch size
  to the latency.
- **Frames per second, FPS** is the ratio of the total number of processed
  images to the total execution time.

### Metrics for the benchmark_app tool (C++ API)

Currently, you can use the `benchmark_app` tool included
in the [Intel® Distribution of OpenVINO™ Toolkit][openvino-toolkit]
to measure the output performance of libraries. The algorithm
for calculating performance indicators is available in the documentation.

## Using the inference_benchmark.py script

```bash
python3 inference_benchmark.py <arguments>
```

Command line arguments:

- `-с / --config <benchmark_configuration.xml>` is the configuration file
  name containing information about the tests being performed.
- `-r / --result <results.csv>`is the resulting file name.
- `--executor_type`is an environment for executing the benchmark script.
  The parameter takes the follwing values: `host_machine` assumes executing
  in the current environment, `docker_container` assumes executing in
  the appropriate docker container.

Example of launching benchmark in the current environment:

```bash
python3 inference_benchmark.py \
    -r results.csv -c benchmark_configuration.xml \
    --executor_type host_machine
```

Example of launching benchmark in the docker container:

```bash
python3 inference_benchmark.py \
    -r results.csv -c benchmark_configuration.xml \
    --executor_type docker_container
```

## Using OpenVINO Benchmark C++ tool as a measurement tool

### How to build (Linux)

1. Clone the repository. It is recommended to use the stable version from
   the list https://github.com/openvinotoolkit/openvino/releases.

   ```bash
   git clone https://github.com/openvinotoolkit/openvino.git
   git checkout <release_tag>
   cd openvino
   git submodule update --init --recursive
   ```

1. Build OpenVINO following the official instructions
   https://github.com/openvinotoolkit/openvino/wiki/BuildingForLinux.

1. If using the stable version, please, install python wheels
   from the PyPI repository.

   ```bash
   pip install --upgrade pip 
   pip install openvino==<your version, ex 2022.1.0>
   pip install openvino_dev
   pip install openvino_dev[mxnet,caffe,caffe2,onnx,pytorch,tensorflow2]==<your version, ex 2022.1.0>
   ```

1. Run `setupvars.sh`:

   ```bash
   source INSTALL_DIR/setupvars.sh 
   ```

1. Run `./build_samples.sh` in the directory `INSTALL_DIR/samples/cpp`.

### How to use

1. In the configuration file (the section `FrameworkDependent`),
   please, indicate `Mode`: `sync` or `async`;
                    `CodeSource`: `ovbenchmark`;
                    `Runtime`: `cpp`;
                    `Hint`: `none`, `latency` or `throughput`.

1. Find the executable file `benchmark_app` in the following directory.

   ```
   /home/<user>/inference_engine_cpp_samples_build/intel64/Release/benchmark_app
   ```

1. Use this executable file as a parameter for the `inference_benchmark.py`
   script:

   ```bash
   python3 inference_benchmark.py -c <path_to_benchmark_configuration_file.xml> -r result.csv -b /home/<user>/inference_engine_cpp_samples_build/intel64/Release/benchmark_app
   ```

## Using OpenVINO Benchmark Python tool as a measurement tool

### How to build

If you are using the stable version, please, install python wheels
from the PyPI repository.

```bash
pip install --upgrade pip 
pip install openvino==<your version, ex 2022.1.0>
pip install openvino_dev
pip install openvino_dev[mxnet,caffe,caffe2,onnx,pytorch,tensorflow2]==<your version, ex 2022.1.0>
```

### How to use

1. In the configuration file (the section `FrameworkDependent`),
   please, indicate `Mode`: `sync` or `async`;
                    `CodeSource`: `ovbenchmark`;
                    `Runtime`: `python`;
                    `Hint`: `none`, `latency` or `throughput`.

1. Run the `inference_benchmark.py` script.

   ```bash
   python3 inference_benchmark.py -c <path_to_benchmark_configuration_file.xml> -r result.csv
   ```


<!-- LINKS -->
[openvino-toolkit]: https://software.intel.com/en-us/openvino-toolkit
[intel-caffe]: https://github.com/intel/caffe
[intel-tensorflow]: https://www.intel.com/content/www/us/en/developer/articles/guide/optimization-for-tensorflow-installation-guide.html
[tensorflow-lite]: https://www.tensorflow.org/lite
[onnx-runtime]: https://onnxruntime.ai
[mxnet]: https://mxnet.apache.org
[opencv]: https://opencv.org
[pytorch]: https://pytorch.org
[dgl-pytorch]: https://www.dgl.ai
[tvm]: https://tvm.apache.org
[rknn]: https://github.com/rockchip-linux/rknpu2
[spektral]: https://graphneural.network
