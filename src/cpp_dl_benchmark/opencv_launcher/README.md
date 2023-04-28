# OpenCV DNN Benchmark

The tool allows to measure deep learning models inference performance with [OpenCV DNN][opencv-dnn].

## Build OpenCV

To get `OpenCV` you need either download [prebuilt binaries](https://opencv.org/releases/) or build it from sources:
1. Clone repository, checkout to the latest stable release and update submodules:

    ```
    git clone https://github.com/opencv/opencv
    cd opencv
    git checkout 4.7.0
    ```

1. Create `build` directory:
   
    ```
    mkdir build && cd build
    ```

1. Configure it with `cmake`:
   
    ```
    cmake -DCMAKE_INSTALL_PREFIX=install -DCMAKE_BUILD_TYPE=Release -DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF -DBUILD_DOCS=OFF ..
    ```

1. Build and install project:

    ```
    make install -j$(nproc --all)
    ```

## Build OpenCV DNN Benchmark

Set `OpenCV_DIR` environment variable pointing to OpenCV folder with `OpenCVConfig.cmake`
so that cmake can find it during configuration step:

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
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_OPENCV_LAUNCHER=ON <dl-benchmark>/src/cpp_dl_benchmark
    ```

1. Build tool

    ```
    cmake --build .
    ```

Application binaries will be placed into `<path_to_build_directory>/<BUILD_TYPE>/bin` directory, where `BUILD_TYPE` whether `Debug` or `Release`.

## Usage

OpenCV DNN launcher supports models in `ONNX`, `Caffe` and `TensorFlow` formats,
no custom backends are tested for now.

Limitations on the models:
- One input
- FP32 input/output types

Note that not all models are supported by OpenCV DNN module. For more information, refer to the [OpenCV documentation][opencv-dnn].

<!-- LINKS -->
[opencv-dnn]: https://docs.opencv.org/4.7.0/d2/d58/tutorial_table_of_content_dnn.html
