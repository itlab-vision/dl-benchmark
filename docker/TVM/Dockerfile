FROM ubuntu_for_dli

ARG TORCH_VERSION=2.0.1
ARG TORCHVISION_VERSION=0.15.2
ARG TF_VERSION=2.12.0
ARG MXNET_VERSION=1.9.1
ARG ONNX_VERSION=1.14.0

ARG PyTorch
ARG Tensorflow
ARG MXNet
ARG ONNX

RUN pip3 install apache-tvm==0.14.dev264

RUN if [ "${PyTorch}" = "true"  ]; then \
    pip3 install torch==${TORCH_VERSION} torchvision==${TORCHVISION_VERSION}; \
    fi

RUN if [ "$Tensorflow" = "true" ]; then \
    pip3 install tensorflow==${TF_VERSION}; \
    fi

RUN if [ "$MXNet" = "true"  ]; then \
    pip3 install mxnet==${MXNET_VERSION}; \
    pip uninstall -y numpy && pip install numpy==1.23.1; \
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
    pip3 install onnxruntime==${ONNX_VERSION} && pip3 install onnx==${ONNX_VERSION}; \
    fi

WORKDIR /tmp/
