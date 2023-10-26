#!/bin/bash

# BUILD_DIR - directory for build ncnn (recommended: ${HOME}/ncnn_build)
# INSTALL_PREFIX - directory for install ncnn (recommended: /usr/local)

BUILD_DIR=${1:-""}
INSTALL_PREFIX=${2:-""}

if [ -z "$BUILD_DIR" ]; then
    echo "Error: Please set build directory as first argument"
    exit 1
fi

if [ -z "$INSTALL_PREFIX" ]; then
    echo "Error: Please set install prefix as second argument"
    exit 1
fi

mkdir "${BUILD_DIR}"
cd "${BUILD_DIR}" || exit

git clone https://github.com/Tencent/ncnn.git
cd ncnn && git submodule update --init

mkdir build && cd build || exit
cmake -DCMAKE_BUILD_TYPE=Release -DNCNN_VULKAN=ON -DNCNN_SYSTEM_GLSLANG=ON -DNCNN_BUILD_EXAMPLES=ON ..
make "-j$(nproc)"
make install
mkdir "${INSTALL_PREFIX}/lib/ncnn"
cp -r "install/include/ncnn" "${INSTALL_PREFIX}/include/ncnn" && cp -r "install/lib/libncnn.a" "${INSTALL_PREFIX}/lib/ncnn/libncnn.a"
printf "PATH=${PATH}:${INSTALL_PREFIX}" | tee -a /etc/bash.bashrc
printf "PATH=${LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}/lib" | tee -a /etc/bash.bashrc
