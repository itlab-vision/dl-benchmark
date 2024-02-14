FROM ubuntu:22.04
USER root
WORKDIR /

# Install Packages
RUN apt update && apt upgrade -y && apt install -y \
    apt-utils autoconf automake build-essential curl nano fdupes \
    git ca-certificates crossbuild-essential-riscv64 \
    gcc-riscv64-linux-gnu g++-riscv64-linux-gnu \
    gcc g++ python3.10 python3-pip python3.10-venv python3.10-dev && \
    rm -rf /var/lib/apt/lists/*

# Install RISC-V packages
RUN dpkg --add-architecture riscv64 && \
    sed -i -E 's|^deb ([^ ]+) (.*)$|deb [arch=amd64] \1 \2\ndeb [arch=riscv64] http://ports.ubuntu.com/ubuntu-ports/ \2|' /etc/apt/sources.list && \
    apt update -y && apt install -y --no-install-recommends libpython3-dev:riscv64

# Install cmake
RUN python3 -m pip install --upgrade pip && python3 -m pip install cmake

# Clone openvino
RUN git clone https://github.com/openvinotoolkit/openvino.git --branch 2023.3.0
WORKDIR /openvino
RUN git submodule update --init \
        ./thirdparty/pugixml \
        ./thirdparty/ade \
        ./thirdparty/gflags/gflags \
        ./thirdparty/protobuf \
        ./thirdparty/json/nlohmann_json \
        ./thirdparty/flatbuffers/flatbuffers \
        ./thirdparty/onnx/onnx \
        ./thirdparty/snappy \
        ./thirdparty/zlib \
        ./thirdparty/open_model_zoo \
        ./src/plugins/intel_cpu/thirdparty/onednn \
        ./src/bindings/python/thirdparty/pybind11

# Copy CMake toolchain
COPY riscv64.toolchain.cmake ./cmake/toolchains/custom_riscv64.toolchain.cmake

# Add RISC-V support to Python Wheel
COPY riscv64.wheel.diff ./riscv64.wheel.diff
RUN git apply ./riscv64.wheel.diff

## Build OpenVINO
RUN python3 -m pip install -r ./src/bindings/python/wheel/requirements-dev.txt
RUN python3 -m pip install -r ./src/bindings/python/src/compatibility/openvino/requirements-dev.txt
RUN mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/openvino_riscv64_gnu -DCMAKE_TOOLCHAIN_FILE=/openvino/cmake/toolchains/custom_riscv64.toolchain.cmake \
    -DENABLE_INTEL_CPU=ON -DENABLE_INTEL_GPU=OFF -DENABLE_INTEL_GNA=OFF -DENABLE_MULTI=OFF -DENABLE_AUTO=OFF -DENABLE_HETERO=OFF \
    -DENABLE_PYTHON=ON -DPYTHON_MODULE_EXTENSION=$(riscv64-linux-gnu-python3-config --extension-suffix) \
    -DPYBIND11_PYTHON_EXECUTABLE_LAST=/usr/bin/python3.10 -DENABLE_PYTHON_PACKAGING=ON && \
    make install -j $(proc)
RUN rm -rf ./build
WORKDIR /
