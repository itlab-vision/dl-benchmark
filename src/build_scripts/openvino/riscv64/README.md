# OpenVINO Cross-Compilation for RISC-V

## Build using Docker

1. Install and configure Docker using [guide](../../../../docker/README).

1. Build Docker image.

   ```bash
   docker build -t openvino_riscv .
   ```

1. Run temporary Docker container using the built image to
   copy the installed OpenVINO libraries on host machine.

   ```bash
   docker run -t openvino_riscv
   docker cp <container_name>:/openvino_riscv64_gnu .
   ```

1. Archive the folder `openvino_riscv64_gnu` and copy on the target
   platform RISC-V using `scp` utility or USB flash drive.

   ```bash
   tar -cvf openvino_riscv64_gnu.tar openvino_riscv64_gnu/
   scp openvino_riscv64_gnu.tar <user>@<address>:<path>
   ```

1. On the target platform unarchive the files and activate OpenVINO environment.

   ```bash
   tar -xvf openvino_riscv64_gnu.tar
   source openvino_riscv64_gnu/setupvars.sh
   ```

1. To check correctness of build try to import `openvino` package.

   ```bash
   python3 -c 'import openvino'
   ```

## Manual build

1. Clone [OpenVINO][ov_repo] repository.

   ```bash
   git clone https://github.com/openvinotoolkit/openvino.git --branch 2023.2.0 && cd openvino
   git submodule update --init \
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
   ```

1. Install RISC-V packages.

   ```bash
   sudo apt-get install -y gcc-riscv64-linux-gnu g++-riscv64-linux-gnu crossbuild-essential-riscv64
   sudo dpkg --add-architecture riscv64
   sudo sed -i -E 's|^deb ([^ ]+) (.*)$|deb [arch=amd64] \1 \2\ndeb [arch=riscv64] http://ports.ubuntu.com/ubuntu-ports/ \2|' /etc/apt/sources.list
   apt update -y && apt install -y --no-install-recommends libpython3-dev:riscv64
   ```

1. Install python requirements.

   ```bash
   python3 -m pip install -r ./src/bindings/python/wheel/requirements-dev.txt
   python3 -m pip install -r ./src/bindings/python/src/compatibility/openvino/requirements-dev.txt
   ```

1. Copy custom CMake toolchain file to repository.

   ```bash
   cp <path>/custom_riscv64.toolchain.cmake <path>/openvino/cmake/toolchains/custom_riscv64.toolchain.cmake
   ```

1. Build OpenVINO from source.

   ```bash
   mkdir build && cd build
   cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=../../openvino_riscv64_gnu \
            -DCMAKE_TOOLCHAIN_FILE=../cmake/toolchains/custom_riscv64.toolchain.cmake \
            -DENABLE_INTEL_CPU=ON -DENABLE_INTEL_GPU=OFF -DENABLE_INTEL_GNA=OFF -DENABLE_MULTI=OFF \
            -DENABLE_AUTO=OFF -DENABLE_HETERO=OFF \
            -DENABLE_PYTHON=ON -DPYTHON_MODULE_EXTENSION=$(riscv64-linux-gnu-python3-config --extension-suffix) \
            -DPYBIND11_PYTHON_EXECUTABLE_LAST=/usr/bin/python3.10 -DENABLE_PYTHON_PACKAGING=ON
   make install -j $(proc)
   rm -rf ./build
   ```

1. The build OpenVINO libraries are stored in the folder `openvino_riscv64_gnu`.
   To copy these files, follow the instructions in the 'Building with Docker' section above.

## Notes

Please note that the versions of Python used to build the OpenVINO Python API and those installed on the RISC-V platform must be the same.


<!-- LINKS -->
[ov_repo]: https://github.com/openvinotoolkit/openvino
