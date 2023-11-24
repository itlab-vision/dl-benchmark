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
RUN python3 -m pip install pycocotools docker PyYAML
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6
RUN python3 -m pip install gluoncv[full]
RUN python3 -m pip install opencv-python
   
# Installing Apache-TVM 
RUN python3 -m pip install apache-tvm==0.14.dev264

# ARG
ARG TORCH_VERSION=2.0.1
ARG TORCHVISION_VERSION=0.15.2
ARG TFLite_VERSION=2.14.0
ARG MXNET_VERSION=1.9.1
ARG ONNX_VERSION=1.15.0
ARG CAFFE_VERSION=1.1.0

ARG PyTorch
ARG TFLite
ARG MXNet
ARG ONNX
ARG CAFFE

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

RUN if [ "$CAFFE" = "true"  ]; then \
    /bin/bash -c "conda install -n tvm-env -y -c intel openvino-ie4py-ubuntu20=2022.1.0"; \
    /bin/bash -c "conda install -n tvm-env -y -c intel scikit-image=0.17.2"; \
    /bin/bash -c "conda install -n tvm-env -y -c intel caffe"; \
    /bin/bash -c "conda install -n tvm-env -y -c anaconda libgcc-ng=11.2.0"; \
    /bin/bash -c "conda install -n tvm-env -y -c defaults protobuf=3.17.2 libprotobuf=3.17.2 requests=2.27.1"; \
    fi
    
WORKDIR /tmp/
