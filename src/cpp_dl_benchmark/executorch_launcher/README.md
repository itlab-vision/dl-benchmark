# ExecuTorch Benchmark
The tool allows to measure deep learning models inference performance with [ExecuTorch][executorch].

## Build ExecuTorch for Linux

1. Create conda environment and activate it.

   ```bash
   conda create -y -n executorch_env python=3.10
   conda activate executorch_env
   ```

1. Clone ExecuTorch repository and update submodules.

   ```bash
   git clone -b v0.5.0 https://github.com/pytorch/executorch
   cd executorch && git submodule update --init
   ```

1. Install requirements for Python.

   ```bash
   ./install_requirements.sh
   ```

1. Configure it with cmake:

   ```bash
   mkdir build && cd build
   cmake -DCMAKE_INSTALL_PREFIX=<install_prefix> \
         -DEXECUTORCH_BUILD_EXTENSION_MODULE=ON \
         -DEXECUTORCH_BUILD_EXTENSION_RUNNER_UTIL=ON \
         -DEXECUTORCH_BUILD_EXTENSION_TENSOR=ON \
         -DEXECUTORCH_BUILD_DEVTOOLS=ON \
         -DBUILD_EXECUTORCH_PORTABLE_OPS=ON \
         -DEXECUTORCH_BUILD_XNNPACK=ON ../
   ```

1. Build and install.

   ```bash
   make "-j$(nproc)" && make install
   ```

## Build ExecuTorch Benchmark

To build the tool you need to have an installation of [ExecuTorch][executorch] and [OpenCV][opencv].
Set the following environment variables so that CMake was able to find them during configuration step.

- `EXECUTORCH_INSTALL_DIR` pointing to the install directory of ExecuTorch.
- `OpenCV_DIR` pointing to the OpenCV folder with `OpenCVConfig.cmake`.

1. Clone repository and update submodules.

   ```bash
   git clone https://github.com/itlab-vision/dl-benchmark
   cd dl-benchmark
   git submodule update --init --recursive
   ```

1. Create `build` directory.

   ```bash
   mkdir build && cd build
   ```

1. In the created directory run `cmake` command.

   ```bash
   cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_EXECUTORCH_LAUNCHER=ON <dl-benchmark>/src/cpp_dl_benchmark
   ```

1. Build tool.

   ```bash
   cmake --build .
   ```

Application binaries will be placed into `<path_to_build_directory>/<BUILD_TYPE>/bin` directory, where
`BUILD_TYPE` whether `Debug` or `Release`.

### Basic usage

To run tool with default options you should provide only path to the model file in the `.pte` format.

```bash
./executorch_benchmark -m model.pte
```

By default, the application runs inference on randomly-generated tensors for 60 seconds. For inference
only default provider (`CPU` device) is available for now.

### Inputs

To pass inputs for model use `-i` option.

```bash
./executorch_benchmark -m model.pte -i <path_to_input_data>
```

By default, number of inputs to use determined based on model's batch size. If yout want to run
inference on some images, you can specify the number of files to take with `-nireq` option.

If the model has several inputs, files or folders must be specified for each of the input.

```bash
./executorch_benchmark -m model.pte -i input1:file1 input2:file2 input3:file3
```

### Shape and layout options

To run inference with dynamic model, you must specify the shape for every model's input:

```bash
./executorch_benchmark -m model.pte -i input1:file1 input2:file2 input3:file3 \
                       -shape input1[N,C],input1[N,C],input1[N,C]
```

Or if all inputs have the same shape you could pass just `-shape [N,C]`. The same rules
are valid to the `-layout` option.


<!-- LINKS -->
[executorch]: https://pytorch.org/executorch-overview
[opencv]: https://github.com/opencv/opencv
