#!/bin/bash

WORKSPACE=${WORKSPACE:-"/opt/ncnn_build"}
mkdir ${WORKSPACE}
cd ${WORKSPACE}

# Install packages
apt update
apt install build-essential git cmake libprotobuf-dev protobuf-compiler libvulkan-dev libopencv-dev mesa-vulkan-drivers vulcan-tools autoconf automake libtool curl make g++ unzip

# Install protobuf
git clone https://github.com/protocolbuffers/protobuf.git -b v4.24.4
cd protobuf && git submodule update --init --recursive

cmake . -DCMAKE_CXX_STANDARD=14
cmake --build . --parallel 8
ctest --verbose
cmake --install .

# Install OpenCV

cd ${WORKSPACE}
wget https://github.com/opencv/opencv/archive/4.8.0.zip && unzip 4.8.0.zip && cd opencv-4.8.0/

mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j8
make install

echo "include /usr/local/lib" | tee -a /etc/ld.so.conf
ldconfig
printf "PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig\nexport PKG_CONFIG_PATH\n" | tee -a /etc/bash.bashrc
