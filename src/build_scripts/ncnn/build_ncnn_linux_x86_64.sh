#!/bin/bash

WORKSPACE=${WORKSPACE:-"/opt/ncnn_build"}
mkdir ${WORKSPACE}
cd ${WORKSPACE}

git clone https://github.com/Tencent/ncnn.git
cd ncnn && git submodule update --init

mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -DNCNN_VULKAN=ON -DNCNN_SYSTEM_GLSLANG=ON -DNCNN_BUILD_EXAMPLES=ON ..
make -j8
make install
mkdir /usr/local/lib/ncnn
cp -r install/include/ncnn /usr/local/include/ncnn && cp -r install/lib/libncnn.a /usr/local/lib/ncnn/libncnn.a
