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
                  ca-certificates \
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
                  ninja-build \
                  ffmpeg \
                  libsm6 \
                  libxext6"
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

# Install openvino
RUN pip3 install --upgrade pip
ARG OV_SHORT_VERSION=2022.3.1
RUN pip3 install openvino==${OV_SHORT_VERSION}

# Install openvino-dev
WORKDIR /tmp/
RUN pip3 install openvino-dev==${OV_SHORT_VERSION}

# Download DLI source code
WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark.git --depth 1 && \
    pip3 install docker PyYAML

# accuracy-check
ARG OMZ_VERSION=2022.3.0
WORKDIR /tmp/
RUN git clone --recursive https://github.com/openvinotoolkit/open_model_zoo.git --branch ${OMZ_VERSION} --single-branch --depth 1
