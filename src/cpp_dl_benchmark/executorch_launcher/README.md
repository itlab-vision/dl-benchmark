# ExecuTorch Benchmark
The tool allows to measure deep learning models inference performance with [ExecuTorch][executorch].

## Build ExecuTorch for Linux

1. Create conda environment:
```bash
conda create -y -n executorch_env python=3.10
```
```bash
conda activate executorch_env
```

2. Clone ExecuTorch repository:
```bash
git clone -b v0.5.0 https://github.com/pytorch/executorch
```
```bash
cd executorch && git submodule update --init
```

3. Install requirements for Python:
```bash
./install_requirements.sh
```

4. Configure it with cmake:
```bash
mkdir build1 && cd build1
```
```bash
cmake -DCMAKE_INSTALL_PREFIX=<install_prefix> \
      -DEXECUTORCH_BUILD_EXTENSION_MODULE=ON \
      -DEXECUTORCH_BUILD_EXTENSION_RUNNER_UTIL=ON \
      -DEXECUTORCH_BUILD_EXTENSION_TENSOR=ON \
      -DEXECUTORCH_BUILD_DEVTOOLS=ON \
      -DBUILD_EXECUTORCH_PORTABLE_OPS=ON \
      -DEXECUTORCH_BUILD_XNNPACK=ON ../
```

5. Build and install:
```bash
make "-j$(nproc)" && make install
```

## Build ExecuTorch Benchmark

To build the tool you need to have an installation of [ExecuTorch][executorch] and [OpenCV][opencv]. Set the following environment variables so that cmake can find them during configuration step:
* `EXECUTORCH_INSTALL_DIR` pointing to ExecuTorch install directory.
* `OpenCV_DIR` pointing to OpenCV folder with `OpenCVConfig.cmake`.

1. Clone repository and update submodules:

    ```
    git clone https://github.com/itlab-vision/dl-benchmark
    cd dl-benchmark
    git submodule update --init --recursive
    ```

1. Create `build` directory:

    ```
    mkdir build && cd build
    ```

1. In the created directory run `cmake` command:

      ```
      cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_EXECUTORCH_LAUNCHER=ON <dl-benchmark>/src/cpp_dl_benchmark
      ```

1. Build tool

    ```
    cmake --build .
    ```

Application binaries will be placed into `<path_to_build_directory>/<BUILD_TYPE>/bin` directory, where `BUILD_TYPE` whether `Debug` or `Release`.

### Basic usage

To run tool with default options you should provide only path to model file in `.pte` format

```
./executorch_benchmark -m model.pte
```
By default, the application makes inference on randomly-generated tensors for 60 seconds. For inference only default provider (`CPU` device) is available for now.

### Inputs

To pass inputs for model use `-i` option.

```
./executorch_benchmark -m model.pte -i <path_to_input_data>
```

By default, number of inputs to use determined based on model's batch size. If yout want to make inference on some files set, you can specify the number of files to take with `-nireq` option.

If the model has several inputs, files or folders must be specified for each:

```
./executorch_benchmark -m model.pte -i input1:file1 input2:file2 input3:file3
```

### Shape and layout options

To make inference with dynamic model, you must specify shape for every model's input:

```
./executorch_benchmark -m model.pte -i input1:file1 input2:file2 input3:file3 -shape input1[N,C],input1[N,C],input1[N,C]
```
Or if all inputs have the same shape you could pass just `-shape [N,C]`. The same rules are applied to `-layout` option.


<!-- LINKS -->
[executorch]: https://pytorch.org/executorch-overview
[opencv]: https://github.com/opencv/opencv