# OpenCV DNN Benchmark
The tool allows to measure deep learning models inference performance with [ONNX Runtime](https://github.com/microsoft/onnxruntime).


## Build OpenCV DNN Benchmark
To build the tool you need to have an installation of [OpenCV](https://github.com/opencv/opencv). Set the following environment variables so that cmake can find them during configuration step:
* `OpenCV_DIR` pointing to OpenCV folder with `OpenCVConfig.cmake`.

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
```
cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_OPENCV_LAUNCHER=ON <dl-benchmark>/src/cpp_dl_benchmark
```

4. Run `cmake --build`
```
cmake --build .
```
Application binaries will be placed into `<path_to_build_directory>/<BUILD_TYPE>/bin` directory, where `BUILD_TYPE` whether `Debug` or `Release`.

## Usage
OpenCV DNN launcher supports models in `ONNX`, `Caffe` and `TensorFlow` formats.
Limitations on the models:
- One input
- FP32 input/output types
Note that not all models are supported by OpenCV DNN module. For more information, refer to the [OpenCV documentation](https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html).
