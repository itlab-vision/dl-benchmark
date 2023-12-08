# Pytorch Benchmark

The tool allows to measure deep learning models inference performance with C++ distribution of [PyTorch][pytorch].

## Build Pytorch

You can download C++ distribution of PyTorch from official [site][pytorch]
(cxx11 ABI needed, for NVIDIA GPU select distribution for CUDA),
or build it from sources ([official instruction][build-instruction]):

1. Clone Pytorch repo:

    ```bash
    git clone --recursive https://github.com/pytorch/pytorch
    cd pytorch
    ```

1. Create `build` directory:

    ```bash
    mkdir build && cd build
    ```

1. Configure it with `cmake`:

    ```bash
    cmake -DBUILD_SHARED_LIBS:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Release -DPYTHON_EXECUTABLE:PATH=`which python3` -DCMAKE_INSTALL_PREFIX:PATH=../pytorch-install ../pytorch
    ```

1. Run build:

    ```bash
    cmake --build . --target install
    ```

## Build PyTorch Benchmark

Set the following environment variables so that cmake can find them during configuration step:
* `Torch_DIR` pointing to LibTorch distribution folder with `TorchConfig.cmake`.
* `OpenCV_DIR` pointing to OpenCV folder with `OpenCVConfig.cmake`.
so that cmake can find it during configuration step:

1. Clone repository and update submodules:

    ```bash
    git clone https://github.com/itlab-vision/dl-benchmark
    cd dl-benchmark
    git submodule update --init --recursive
    ```

1. Create `build` directory:

    ```bash
    mkdir build && cd build
    ```

1. In the created directory run `cmake` command:

    - For PyTorch with default settings:

        ```bash
        cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_PYTORCH_LAUNCHER=ON \
            -DTorch_DIR=<PyTorch_DIR>/share/cmake/Torch/ \
            <dl-benchmark>/src/cpp_dl_benchmark
        ```
    - For Torch-TensorRT:

        ```bash
        cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_PYTORCH_TENSORRT_LAUNCHER=ON \
            -DTorch_DIR=<PyTorch_DIR>/share/cmake/Torch/ \
            -DTORCH_TENSORRT_DIR=<Torch-TensorRT_DIR> \
            <dl-benchmark>/src/cpp_dl_benchmark
        ```

1. Build tool

    ```bash
    cmake --build . -- -j$(nproc --all)
    ```

Application binaries will be placed into `<path_to_build_directory>/<BUILD_TYPE>/bin` directory, where `BUILD_TYPE` whether `Debug` or `Release`.

## Usage

Pytorch launcher supports TorchScript representation of PyTorch models (`.pt`). LibTorch doesn't provide interface to get models inputs/ouputs information (such as names, shapes, data type, layout), so it's necessary to provide all of this explicitly from the command line. To know the full list of command line argumets, run the tool with `-h` argumet.

<!-- LINKS -->
[pytorch]: https://pytorch.org/
[build-instruction]: https://github.com/pytorch/pytorch/blob/main/docs/libtorch.rst