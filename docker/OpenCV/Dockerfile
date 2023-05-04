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
                  cmake \
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

# Install OpenVINO
ARG OV_SHORT_VERSION=2022.3
ARG OV_LONG_VERSION="${OV_SHORT_VERSION}.0.9052.9752fafe8eb_x86_64"
RUN sudo mkdir /opt/intel && \
    wget https://storage.openvinotoolkit.org/repositories/openvino/packages/${OV_SHORT_VERSION}/linux/l_openvino_toolkit_ubuntu20_${OV_LONG_VERSION}.tgz \
        -O /tmp/openvino.tgz --no-check-certificate --quiet && \
    tar -zxvf /tmp/openvino.tgz -C /opt/intel/ && \
    sudo ln -s /opt/intel/l_openvino_toolkit_ubuntu20_${OV_LONG_VERSION} /opt/intel/openvino_2022 && \
    rm -rf /tmp/*

# Install OpenVINO dependencies
ENV INSTALL_DIR /opt/intel/openvino_2022
WORKDIR $INSTALL_DIR/install_dependencies
RUN ls -la /opt/intel/openvino_2022/install_dependencies && echo y | ./install_openvino_dependencies.sh
RUN cat /root/.bashrc > tmp && echo 'source $INSTALL_DIR/setupvars.sh' > /root/.bashrc

# Configure for GPU, MYRIAD
RUN echo y | ./install_NEO_OCL_driver.sh
RUN usermod -a -G video,users root

# Install openvino-dev
WORKDIR /tmp/
RUN pip3 install --upgrade pip
RUN pip3 install openvino-dev==2022.3

# Install OpenCV
RUN pip uninstall opencv-python -y
RUN git clone --recurse-submodules https://github.com/opencv/opencv.git  --depth 1 --branch 4.x --single-branch
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

#accuracy-check
WORKDIR /tmp/
RUN git clone --recursive https://github.com/openvinotoolkit/open_model_zoo.git --branch 2022.3.0 --single-branch --depth 1
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN /bin/bash -c 'source $INSTALL_DIR/setupvars.sh && \
    accuracy_check -c sample/sample_config.yml -m data/test_models -s sample'

# Download DLI source code
WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark.git --depth 1 && \
    pip3 install docker PyYAML

# Download dataset if repository with dataset is set
ARG DATASET_DOWNLOAD_LINK
RUN if [ -z "$DATASET_DOWNLOAD_LINK" ] ; then echo Argument DATASET_DOWNLOAD_LINK not provided ; else git clone $DATASET_DOWNLOAD_LINK ; fi