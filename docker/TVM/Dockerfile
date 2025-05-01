FROM ubuntu_for_dli

WORKDIR /root/

# Installing miniconda
RUN wget -q --no-check-certificate -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b && \
    ./miniconda3/bin/conda create -n tvm-env -y python=3.7.16 && \
    rm -rf /root/miniconda3/pkgs/* && \
    rm ~/Miniconda3-latest-Linux-x86_64.sh -f

ENV PATH /root/miniconda3/envs/tvm-env/bin:/root/miniconda3/bin:$PATH
RUN echo "source activate tvm-env" > ~/.bashrc
RUN export LD_LIBRARY_PATH=/root/miniconda3/envs/tvm-env/lib:${LD_LIBRARY_PATH}
RUN conda config --add channels intel

# Installing dependencies
RUN python3 -m pip install pycocotools docker PyYAML gluoncv[full] opencv-python Cython psutil
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6
RUN apt-get update && apt-get install -y -qq --no-install-recommends cmake software-properties-common
RUN apt-add-repository "deb http://apt.llvm.org/jammy/ llvm-toolchain-jammy-19 main" && \
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | sudo apt-key add -
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends llvm-19 llvm-19-dev && \
    rm -rf /var/lib/apt/lists/*

# Installing Apache-TVM 
ARG TVM_VERSION=v0.20.0

RUN git clone --recursive https://github.com/apache/tvm tvm --branch ${TVM_VERSION} --single-branch
ENV TVM_BUILD_DIR=/tmp/build-tvm
RUN mkdir $TVM_BUILD_DIR && cd $TVM_BUILD_DIR
RUN cp /root/tvm/cmake/config.cmake .
RUN echo "set(CMAKE_BUILD_TYPE RelWithDebInfo)" >> config.cmake
RUN echo "set(USE_LLVM /usr/bin/llvm-config-19)" >> config.cmake
RUN echo "set(HIDE_PRIVATE_SYMBOLS ON)" >> config.cmake
RUN echo "set(USE_CUDA    OFF)" >> config.cmake
RUN echo "set(USE_METAL   OFF)" >> config.cmake
RUN echo "set(USE_VULKAN  OFF)" >> config.cmake
RUN echo "set(USE_OPENCL  OFF)" >> config.cmake
RUN echo "set(USE_CUBLAS  OFF)" >> config.cmake
RUN echo "set(USE_CUDNN   OFF)" >> config.cmake
RUN echo "set(USE_CUTLASS OFF)" >> config.cmake

RUN /bin/bash -c 'cmake /root/tvm/ && cmake --build . -- -j$(nproc --all)'

WORKDIR /root/
RUN export TVM_LIBRARY_PATH=$TVM_BUILD_DIR
RUN python3 -m pip install -e /root/tvm/python

# ARG
ARG TORCH_VERSION=2.0.1
ARG TORCHVISION_VERSION=0.15.2
ARG TFLite_VERSION=2.14.0
ARG MXNET_VERSION=1.9.1
ARG ONNX_VERSION=1.15.0

ARG PyTorch
ARG TFLite
ARG MXNet
ARG ONNX

RUN if [ "${PyTorch}" = "true"  ]; then \
    python3 -m pip install torch==${TORCH_VERSION} torchvision==${TORCHVISION_VERSION}; \
    fi
    
RUN if [ "$TFLite" = "true" ]; then \
    python3 -m pip install tflite-runtime==${TFLite_VERSION}; \
    fi
    
RUN if [ "$MXNet" = "true"  ]; then \
    python3 -m pip install mxnet==${MXNET_VERSION}; \
    python3 -m pip uninstall -y numpy && python3 -m pip install numpy==1.23.1; \
    fi

RUN if [ "$ONNX" = "true"  ]; then \
    git clone https://github.com/microsoft/onnxruntime.git; \
    cd onnxruntime; \ 
    git checkout v${ONNX_VERSION}; \ 
    git submodule update --init --recursive && mkdir build && cd build; \
    cmake -DCMAKE_INSTALL_PREFIX=install \
        -DCMAKE_BUILD_TYPE=Release \
        -Donnxruntime_BUILD_FOR_NATIVE_MACHINE=ON \
        -Donnxruntime_BUILD_UNIT_TESTS=OFF \
        -Donnxruntime_BUILD_SHARED_LIB=ON \
        -Donnxruntime_USE_FULL_PROTOBUF=ON ../cmake; \ 
    make install -j$(nproc --all); \
    python3 -m pip install onnxruntime==${ONNX_VERSION} && python3 -m pip install onnx==${ONNX_VERSION}; \
    fi

WORKDIR /tmp/open_model_zoo/
RUN git remote add omz_custom_tvm https://github.com/itlab-vision/open_model_zoo_tvm.git && \ 
    git fetch omz_custom_tvm && \
    git checkout omz_custom_tvm/24.3.0/tvm
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN python3 setup.py install_core

WORKDIR /tmp/
