# CPP DL Benchmark

The tool allows to measure deep learning models inference performance with various inference frameworks. This implementation inspired by [OpenVINO Benchmark C++ tool][benchmark-app] as a reference and stick to its measurement methodology, thus provides consistent performance results.

## Common prerequisites

The tool was tested on Ubuntu 20.04 (64-bit) with default GCC* 9.4.0
1. CMake 3.16 or higher
1. GCC 9.4 or higher
1. nlohmann-json library

    ```
    sudo apt install nlohmann-json3-dev
    ```

## Supported inference frameworks

1. [ONNX Runtime](onnxruntime_launcher/README.md)
1. [OpenCV DNN](opencv_launcher/README.md)
1. [TensorFlow Lite](tflite_launcher/README.md)
1. [PyTorch](pytorch_launcher/README.md)
1. [RKNN](rknn_launcher/README.md)

## Build

To build specific launcher please refer to the corresponding `README.md` file in the launcher directory. By default all launchers will be built.

## Usage

Running the tool  with `-h` option shows the help message:

```
<framework>_benchmark
Options:
        [-h]                                          show the help message and exit
        [-help]                                       print help on all arguments
         -m <MODEL FILE>                              path to a file with a trained model or a config file.
                                                      available formats (depends on benchmark build):
                                                          ONNX Runtime - .onnx
                                                          OpenCV - .xml, .onnx, .pb, .protoxt
                                                          TF Lite - .tflite
                                                          Pytorch - .pt
                                                          RKNN - .rknn
        [-w <WEIGHTS FILE>]                           path to a model weights file.
                                                      available formats:
                                                          OpenCV - .caffemodel, .bin
        [-i <INPUT>]                                  path to an input to process. The input must be an image and/or binaries, a folder of images and/or binaries.
                                                      ex.: "input1:file1 input2:file2 input3:file3" or just path to the file or folder if model has one input
        [-d <DEVICE>]                                 target device to infer on. Avalaibale devices depends on the framework:
                                                          ONNX Runtime: CPU, CUDA (CUDA EP)
                                                          OpenCV: CPU, GPU
        [-b <NUMBER>]                                 batch size value. If not provided, batch size value is determined from the model
        [--shape <[N,C,H,W]>]                         shape for network input.
                                                      ex., "input1[1,128],input2[1,128],input3[1,128]" or just "[1,3,224,224]"
        [--layout <[NCHW]>]                           layout for network input.
                                                      ex.: "input1[NCHW],input2[NC]" or just "[NCHW]"
        [--dtype <[FP32]>]                            data type of network input.
                                                      ex.: "input1[FP32],input2[FP32]" or just "[FP32]"
        [--mean <R G B>]                              mean values per channel for input image.
                                                      applicable only for models with image input.
                                                      ex.: [123.675,116.28,103.53] or with specifying inputs src[255,255,255]
        [--scale <R G B>]                             scale values per channel for input image.
                                                      applicable only for models with image inputs.
                                                      ex.: [58.395,57.12,57.375] or with specifying inputs src[255,255,255]
        [--channel_swap]                              switch the input channels order from BGR to RGB.
                                                      applicable only for models with image inputs.
                                                      image are uploaded in BGR format by default
        [--nthreads <NUMBER>]                         number of threads to utilize.
        [--nireq <NUMBER>]                            number of inference requests. If not provided, default value is set.
        [--niter <NUMBER>]                            number of iterations. If not provided, default time limit is set.
        [-t <NUMBER>]                                 time limit for inference in seconds
        [--fps <NUMBER>]                              fps limit for inference; if actual model inference is faster than the desired fps, it slows down with a condvar wait_for call.
        [--save_report]                               save report in JSON format.
        [--report_path <PATH>]                        destination path for report.
        [--dump_output]                               save final tensor value.
        [--output_path <PATH>]                        destination path for output
```

<!-- LINKS -->
[benchmark-app]: https://github.com/openvinotoolkit/openvino/tree/master/samples/cpp/benchmark_app
