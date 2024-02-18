FROM ubuntu:22.04
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
                  ca-certificates \
                  sudo \
                  automake \
                  build-essential \
                  cpio \
                  curl \
                  dialog \
                  gnupg2 \
                  libdrm2 \
                  libglib2.0-0 \
                  lsb-release \
                  libtool \
                  libprotobuf-dev \
                  ninja-build \
                  libgl1-mesa-glx \
                  nlohmann-json3-dev \
                  python3-pip \
                  python3-setuptools \
                  python3-dev \
                  python3-venv \
                  libpython3.10 \
                  udev \
                  unzip \
                  wget \
                  git \
                  ninja-build \
                  ffmpeg"
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

# Install openvino
RUN pip3 install --upgrade pip
ARG OV_SHORT_VERSION=2023.0.2
RUN pip3 install openvino==${OV_SHORT_VERSION}

# Install openvino-dev
WORKDIR /tmp/
RUN pip3 install openvino-dev==${OV_SHORT_VERSION} docker PyYAML

# Download DLI source code
WORKDIR /tmp/
ARG DLI_BRANCH="master"
RUN git clone --recursive https://github.com/itlab-vision/dl-benchmark.git --branch ${DLI_BRANCH} --single-branch --depth 1

# accuracy-check
WORKDIR /tmp/
RUN git clone --recursive https://github.com/openvinotoolkit/open_model_zoo.git --branch ${OV_SHORT_VERSION} --single-branch --depth 1
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN wget -q https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample

# Download dataset if repository with dataset is set
WORKDIR /tmp/
ARG DATASET_DOWNLOAD_LINK
RUN if [ -z "$DATASET_DOWNLOAD_LINK" ] ; then echo Argument DATASET_DOWNLOAD_LINK not provided ; else git clone $DATASET_DOWNLOAD_LINK ; fi
