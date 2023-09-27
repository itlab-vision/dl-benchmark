# TensorFlow Lite Benchmark

The tool allows to measure deep learning models inference performance with [TensorFlow Lite][tflite].

## Build TensorFlow Lite

Clone repository, checkout to the `2.13.0` release:

```bash
git clone  https://github.com/tensorflow/tensorflow
cd tensorflow
git checkout v2.13.0
```

### CMake build

1. Create `build` directory:

    ```bash
    mkdir build && cd build
    ```

1. Configure it with `cmake`:

    - For x86 native build:

        ```bash
        cmake -DCMAKE_BUILD_TYPE=Release \
            -DBUILD_SHARED_LIBS=ON \
            -DTFLITE_ENABLE_GPU=ON \
            ../tensorflow/lite
        ```

    - For aarch64 machine with cross-compilation:

      Firstly, install cross-compile tools:

        ```bash
        sudo apt install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
        ```

      Then, configure:

        ```bash
        cmake -DCMAKE_BUILD_TYPE=Release \
            -DBUILD_SHARED_LIBS=ON \
            -DCMAKE_TOOLCHAIN_FILE=<dl-benchmark-repo>/cpp_dl_benchmark/cmake/aarch64_toolchain.cmake \
            -DTFLITE_ENABLE_GPU=ON \
            ../tensorflow/lite
        ```

1. Build project:

    ```bash
    cmake --build . -- -j$(nproc --all)
    ```

   > **NOTE:**
   > In case of cross-compilation, you might need to bring to target machine
   > besides `libtensorflow-lite.so` its dependencies (located in <tflite_build_dir>/_deps):
   > ```
    >libcpuinfo.so
    >libfarmhash.so
    >libfft2d_fftsg.so
    >libfft2d_fftsg2d.so
    >libpthreadpool.so
    >libXNNPACK.so
    >```
   >And GPU delegate dependencies (located in <tflite_build_dir>/_deps/abseil-cpp-build/absl):
   >```
    >libabsl_base.so
    >libabsl_city.so
    >libabsl_cord.so
    >libabsl_cord_internal.so
    >libabsl_cordz_functions.so
    >libabsl_cordz_handle.so
    >libabsl_cordz_info.so
    >libabsl_debugging_internal.so
    >libabsl_demangle_internal.so
    >libabsl_exponential_biased.so
    >libabsl_hash.so
    >libabsl_int128.so
    >libabsl_low_level_hash.so
    >libabsl_malloc_internal.so
    >libabsl_raw_hash_set.so
    >libabsl_raw_logging_internal.so
    >libabsl_spinlock_wait.so
    >libabsl_stacktrace.so
    >libabsl_status.so
    >libabsl_str_format_internal.so
    >libabsl_strerror.so
    >libabsl_strings.so
    >libabsl_strings_internal.so
    >libabsl_symbolize.so
    >libabsl_synchronization.so
    >libabsl_throw_delegate.so
    >libabsl_time.so
    >libabsl_time_zone.so
    >```

>

### Bazel build

Second opiton is to build TF Lite with bazel.

1. (Optional) Install python3 and essential modules:

    ```bash
    sudo apt install python3-dev python3-pip    
    pip install -U --user pip numpy wheel packaging requests opt_einsum
    pip install -U --user keras_preprocessing --no-deps
    ```

1. Install `bazel-5.1.1`

    ```bash
    sudo apt install curl gnupg
    curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg
    sudo mv bazel.gpg /etc/apt/trusted.gpg.d/
    echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
    
    sudo apt update && sudo apt install bazel=5.1.1
    sudo apt update && sudo apt full-upgrade
    bazel --version
    ```

1. Go to `tensorflow` directory:

    ```bash
    cd tensorflow
    ```

1. (Optional) If you need to adjust build settings, you can call `configure` script:

    ```bash
    ./configure
    ```

1. Build with `bazel`:
   > Flex delegate could be built only with bazel

   For x86 Linux:

    ```bash
    bazel build --define tflite_with_xnnpack=true -c opt //tensorflow/lite:libtensorflowlite.so
    bazel build -c opt //tensorflow/lite/c:libtensorflowlite_c.so
    # to enable TensorFlow operators support
    bazel build --config=monolithic -c opt //tensorflow/lite/delegates/flex:tensorflowlite_flex
    ```

   Shared libraries are located at the following paths:

    * `bazel-bin/tensorflow/lite/libtensorflowlite.so`
    * `bazel-bin/tensorflow/lite/c/libtensorflowlite_c.so`
    * `bazel-bin/tensorflow/lite/delegates/flex/libtensorflowlite_flex.so`

   To build GPU delegate, make sure you have installed GPU drivers (e.g. for ubuntu 20.04 Intel GPU instruction could be
   found [here][gpu-drivers]).

   Then run build command:

    ```bash
    bazel build  -c opt --copt=-DCL_DELEGATE_NO_GL --copt=-DMESA_EGL_NO_X11_HEADERS=1 --copt -DEGL_NO_X11=1 //tensorflow/lite/delegates/gpu:libtensorflowlite_gpu_delegate.so
    ```
   GPU delegate shared library is located at the following
   path: `bazel-bin/tensorflow/lite/delegates/gpu/libtensorflowlite_gpu_delegate.so`

   > To cross-build for `aarch64` linux platforms add `--config=elinux_aarch64` to the commands above. Flags that
   disable OpenGL backend: `--copt=-DCL_DELEGATE_NO_GL --copt=-DMESA_EGL_NO_X11_HEADERS=1 --copt -DEGL_NO_X11=1` - could
   be omitted.

## Build TensorFlow Lite Benchmark

Set `OpenCV_DIR` environment variable pointing to OpenCV folder with `OpenCVConfig.cmake`
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

    - For TF Lite with default CPU delegate launcher:

         ```bash
         cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TFLITE_LAUNCHER=ON -DTENSORFLOW_SRC_DIR=<tensorflow-src-dir> -DTFLITE_BUILD_DIR=<tflite-build-dir> <dl-benchmark>/src/cpp_dl_benchmark
         ```

    - For TF Lite with XNNPack delegate launcher:

         ```bash
         cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TFLITE_XNNPACK_LAUNCHER=ON -DTENSORFLOW_SRC_DIR=<tensorflow-src-dir> -DTFLITE_BUILD_DIR=<tflite-build-dir> <dl-benchmark>/src/cpp_dl_benchmark
         ```

   Configuration with TF Lite bazel build:
    ```bash
    cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TFLITE_XNNPACK_LAUNCHER=ON -DTENSORFLOW_SRC_DIR=<tensorflow-src-dir> -DTFLITE_BUILD_DIR=<tensorflow-dir>/bazel-bin/tensorflow/lite <dl-benchmark>/src/cpp_dl_benchmark
    ```

1. Build tool

    ```bash
    cmake --build . -- -j$(nproc --all)
    ```

Application binaries will be placed into `<path_to_build_directory>/<BUILD_TYPE>/bin` directory, where `BUILD_TYPE`
whether `Debug` or `Release`.

## Usage

TensorFlow Lite launcher supports models in `tflite` formats. Some models that require flex delegate may not work on gpu
delegate.

<!-- LINKS -->

[tflite]: https://www.tensorflow.org/lite

[gpu-drivers]: https://dgpu-docs.intel.com/installation-guides/ubuntu/ubuntu-focal.html
