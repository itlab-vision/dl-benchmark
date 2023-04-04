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

2. Create `build` directory:
   
    ```
    mkdir build && cd build
    ```

3. Configure it with `cmake`:
   3.1. For OpenCV with OpenVINO:
        Setup environment variables to detect OpenVINO:
        ```
        source /openvino/bin/setupvars.sh
        ```
        ```
        cmake -DCMAKE_INSTALL_PREFIX=install -DCMAKE_BUILD_TYPE=Release -DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF -D WITH_OPENVINO=ON -DBUILD_DOCS=OFF ..
        ```
   3.2. For OpenCV:
        ```
        cmake -DCMAKE_INSTALL_PREFIX=install -DCMAKE_BUILD_TYPE=Release -DBUILD_EXAMPLES=OFF -DBUILD_TESTS=OFF -DWITH_OPENVINO=OFF -DBUILD_DOCS=OFF ..
        ```

4. Build and install project:

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

2. Create `build` directory:

    ```
    mkdir build && cd build
    ```

3. In the created directory run `cmake` command:
    3.1. For OPENCV_LAUNCHER with OpenVINO:
         ```
         cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_OPENCV_OV_LAUNCHER=ON -DBUILD_ONNXRUNTIME_LAUNCHER=OFF <dl-benchmark>/src/cpp_dl_benchmark
         ```
    3.2. For OPENCV_LAUNCHER:
         ```
         cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_OPENCV_LAUNCHER=ON <dl-benchmark>/src/cpp_dl_benchmark
         ```

4. Build tool

    ```
    cmake --build .
    ```

Application binaries will be placed into `<path_to_build_directory>/<BUILD_TYPE>/bin` directory, where `BUILD_TYPE` whether `Debug` or `Release`.

## Usage

OpenCV DNN launcher supports models in `IR (OpenVINO)`, '`ONNX`, `Caffe` and `TensorFlow` formats,
no custom backends are tested for now.

Limitations on the models:
- One input
- FP32 input/output types

Note that not all models are supported by OpenCV DNN module. For more information, refer to the [OpenCV documentation][opencv-dnn].

<!-- LINKS -->
[opencv-dnn]: https://docs.opencv.org/4.7.0/d2/d58/tutorial_table_of_content_dnn.html
