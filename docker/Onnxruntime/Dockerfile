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

# Install OpenVINO
ENV INSTALL_DIR /opt/intel/openvino_2022
ARG OV_SHORT_VERSION=2022.3
ARG OV_LONG_VERSION="${OV_SHORT_VERSION}.0.9052.9752fafe8eb_x86_64"
RUN sudo mkdir /opt/intel && \
    wget https://storage.openvinotoolkit.org/repositories/openvino/packages/${OV_SHORT_VERSION}/linux/l_openvino_toolkit_ubuntu20_${OV_LONG_VERSION}.tgz \
        -O /tmp/openvino.tgz --no-check-certificate --quiet && \
    tar -zxvf /tmp/openvino.tgz -C /opt/intel/ && \
    sudo ln -s /opt/intel/l_openvino_toolkit_ubuntu20_${OV_LONG_VERSION} $INSTALL_DIR && \
    rm -rf /tmp/*

# Install OpenVINO dependencies
WORKDIR $INSTALL_DIR/install_dependencies
RUN ls -la $INSTALL_DIR/install_dependencies && echo y | ./install_openvino_dependencies.sh
RUN cat /root/.bashrc > tmp && echo 'source $INSTALL_DIR/setupvars.sh' > /root/.bashrc

# Install openvino-dev
WORKDIR /tmp/
RUN pip3 install --upgrade pip
RUN pip3 install openvino-dev==${OV_SHORT_VERSION}

# Install OpenCV
ARG OCV_VERSION=4.7.0
RUN pip uninstall opencv-python -y
RUN git clone --recurse-submodules https://github.com/opencv/opencv.git  --depth 1 --branch ${OCV_VERSION} --single-branch
ENV OpenCV_BUILD_DIR=/root/build-opencv
RUN mkdir $OpenCV_BUILD_DIR
WORKDIR $OpenCV_BUILD_DIR
RUN /bin/bash -c 'source $INSTALL_DIR/setupvars.sh && \
    cmake -G Ninja \
        -D CMAKE_INSTALL_PREFIX=install \
        -D CMAKE_BUILD_TYPE=Release \
        -D BUILD_EXAMPLES=OFF \
        -D BUILD_TESTS=OFF \
        -D BUILD_DOCS=OFF \
        -D WITH_OPENVINO=ON \
        -D OPENCV_LIB_INSTALL_PATH=lib \
        -D OPENCV_CONFIG_INSTALL_PATH=cmake \
        -D PYTHON3_PACKAGES_PATH=install/python/python3 \
        /tmp/opencv/ && ninja && cmake --install .' && \
    rm -rf /tmp/*
ENV OpenCV_INSTALL_DIR="$OpenCV_BUILD_DIR/install"
ENV OpenCV_DIR="$OpenCV_INSTALL_DIR/cmake"
ENV LD_LIBRARY_PATH="$OpenCV_INSTALL_DIR/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
ENV PYTHONPATH="$OpenCV_INSTALL_DIR/python/python3/cv2/python-3.8${PYTHONPATH:+:$PYTHONPATH}"

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

# accuracy-check
ARG OMZ_VERSION="${OV_SHORT_VERSION}.0"
WORKDIR /tmp/
RUN git clone --recursive https://github.com/openvinotoolkit/open_model_zoo.git --branch ${OMZ_VERSION} --single-branch --depth 1
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN /bin/bash -c 'source $INSTALL_DIR/setupvars.sh && \
    accuracy_check -c sample/sample_config.yml -m data/test_models -s sample'

# Download DLI source  code
WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark.git --depth 1 && \
    pip3 install docker PyYAML