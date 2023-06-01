FROM ubuntu:20.04
USER root
WORKDIR /

# Setup timezone
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add user
RUN useradd -ms /bin/bash openvino && \
    chown openvino -R /home/openvino

# Install dependencies
ARG DEPENDENCIES="apt-utils \
                  autoconf \
                  sudo \
                  vim \
                  automake \
                  build-essential \
                  cpio \
                  curl \
                  dialog \
                  gnupg2 \
                  libdrm2 \
                  libglib2.0-0 \
                  lsb-release \
                  libgtk-3-0 \
                  libtool \
                  python3-pip \
                  python3-setuptools \
                  python3-dev \
                  python3-venv \
                  pciutils \
                  libpython3.8 \
                  udev \
                  unzip \
                  wget \
                  git \
                  ninja-build"
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

#install cmake
WORKDIR /tmp/
ARG CMAKE_VERSION=3.24
RUN pip3 install cmake==${CMAKE_VERSION}

#install onnxruntime
WORKDIR /tmp/
ARG ONNX_VERSION=1.14.0
RUN git clone https://github.com/microsoft/onnxruntime.git && \ 
    cd onnxruntime && \ 
    git checkout v${ONNX_VERSION} && \ 
    git submodule update --init --recursive && mkdir build && cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=install \
        -DCMAKE_BUILD_TYPE=Release \
        -Donnxruntime_BUILD_FOR_NATIVE_MACHINE=ON \
        -Donnxruntime_BUILD_UNIT_TESTS=OFF \
        -Donnxruntime_BUILD_SHARED_LIB=ON \
        -Donnxruntime_USE_FULL_PROTOBUF=ON ../cmake && \ 
    make install -j$(nproc --all)
RUN pip3 install onnxruntime==${ONNX_VERSION}
