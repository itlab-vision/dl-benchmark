#!/bin/bash

# BUILD_DIR - directory for build prerequisites (recommended: ${HOME}/ncnn_build)
# INSTALL_PREFIX - directory for install prerequisites (recommended: /usr/local)

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

# Install packages
apt update
apt install build-essential git cmake libprotobuf-dev protobuf-compiler libvulkan-dev libopencv-dev mesa-vulkan-drivers vulcan-tools autoconf automake libtool curl make g++ unzip

# Install protobuf
git clone https://github.com/protocolbuffers/protobuf.git -b v4.24.4
cd protobuf && git submodule update --init --recursive

cmake . -DCMAKE_CXX_STANDARD=14
cmake --build . --parallel "$(nproc)"
ctest --verbose
cmake --install .

# Install OpenCV

cd "${BUILD_DIR}" || eixt
wget https://github.com/opencv/opencv/archive/4.8.0.zip && unzip 4.8.0.zip && cd opencv-4.8.0/ || exit

mkdir build && cd build || exit
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX="${INSTALL_PREFIX}" ..
make "-j$(nproc)"
make install

echo "include ${INSTALL_PREFIX}/lib" | tee -a /etc/ld.so.conf
ldconfig
printf "PKG_CONFIG_PATH=${PKG_CONFIG_PATH}:${INSTALL_PREFIX}/lib/pkgconfig\nexport PKG_CONFIG_PATH\n" | tee -a /etc/bash.bashrc
printf "PATH=${PATH}:${INSTALL_PREFIX}" | tee -a /etc/bash.bashrc
printf "PATH=${LD_LIBRARY_PATH}:${LD_LIBRARY_PATH}/lib" | tee -a /etc/bash.bashrc
