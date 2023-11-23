# RKNN Benchmark

The tool allows to measure deep learning models inference performance on Rockchip NPU with [RKNN API][rknn]. For measurements you'll need a Rockchip device with NPU on board. [RKNPU2][rknn] supports next platforms:
* RK3566/RK3568
* RK3588/RK3588S
* RV1103/RV1106
* RK3562

## Download RKNPU2

Clone repository, checkout to the `1.4.0` release:

```bash
git clone https://github.com/rockchip-linux/rknpu2
cd rknpu2
git checkout v1.4.0
```

## (Optional) Build nlohmann-json for Android

1. Download [Android NDK][NDK]

1. Clone repository:

    ```bash
    git clone https://github.com/nlohmann/json
    cd json
    git checkout v3.11.2
    ```

1. Create build directory:

    ```
    mkdir build && cd build
    ```

1. Build it with toolchain from Android NDK:

    ```bash
    cmake -DCMAKE_BUILD_TYPE=Release
    -DDCMAKE_SYSTEM_PROCESSOR=aarch64,
    -DCMAKE_SYSTEM_VERSION=31,
    -DANDROID_PLATFORM=31, # for Android 12
    -DANDROID_ABI=arm64-v8a,
    -DCMAKE_ANDROID_ARCH_ABI=arm64-v8a,
    -DCMAKE_TOOLCHAIN_FILE=<android-ndk-path>/<ndk-version>/build/cmake/android.toolchain.cmake
    ..
    ```

## Build RKNN Benchmark

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

- For aarch64 Linux: 

    ```bash
    cmake -DCMAKE_TOOLCHAIN_FILE=<dl-benchmark>/src/cpp_dl_benchmark/cmake/aarch64_toolchain.cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_RKNN_LAUNCHER=ON -DRKNN_DIR=<rknpu2_dir> <dl-benchmark>/src/cpp_dl_benchmark
    ```

- For aarch64 Android:

    ```bash
    cmake -DDCMAKE_SYSTEM_PROCESSOR=aarch64,
    -DANDROID_PLATFORM=31, # for Android 12
    -DCMAKE_SYSTEM_VERSION=31,
    -DANDROID_ABI=arm64-v8a,
    -DCMAKE_ANDROID_ARCH_ABI=arm64-v8a,
    -DCMAKE_TOOLCHAIN_FILE=<android-ndk-path>/<ndk-version>/build/cmake/android.toolchain.cmake
    -DCMAKE_BUILD_TYPE=Release -DBUILD_RKNN_LAUNCHER=ON
    -DRKNN_DIR=<rknpu2_dir>
    -Dnlohmann_json_DIR=<nlohmann_json_build>
     <dl-benchmark>/src/cpp_dl_benchmark
    ```

1. Build tool

    ```bash
    cmake --build . -- -j$(nproc --all)
    ```

Application binaries will be placed into `<path_to_build_directory>/<BUILD_TYPE>/bin` directory, where `BUILD_TYPE`
whether `Debug` or `Release`.

## Usage

RKNN launcher supports models in `rknn` formats. Due to benchmark and `RKNN API` specifics, input data type should be provided explicitly from command line.
For example, for images, it should be `U8``:
```
./rknn_benchmark -i img.jpg -m model.rknn --dtype [U8] --channel_swap --dump_output -niter 1
```

<!-- LINKS -->
[rknn]: https://github.com/rockchip-linux/rknpu2
[NDK]: https://developer.android.com/ndk/downloads