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
                  python3-pandas \
                  python3-pip \
                  python3-setuptools \
                  python3-dev \
                  python3-venv \
                  pciutils \
                  libpython3.8 \
                  udev \
                  unzip \
                  wget \
                  git"
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

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
ARG OV_SHORT_VERSION=2022.3
WORKDIR /tmp/
RUN pip3 install --upgrade pip
RUN pip3 install openvino-dev==${OV_SHORT_VERSION}

# Install pycocotools
RUN pip3 install pycocotools

# Install OpenCV dependencies
RUN apt-get install ffmpeg libsm6 libxext6 -y

# Install GluonCV
RUN pip3 install gluoncv[full]

# Install MXNet
ARG MXNET_VERSION=1.9.1
RUN pip3 install mxnet==${MXNET_VERSION}

# Download Accuracy Checker
ARG OMZ_VERSION="${OV_SHORT_VERSION}.0"
WORKDIR /tmp/
RUN git clone --recursive https://github.com/openvinotoolkit/open_model_zoo.git --branch ${OMZ_VERSION} --single-branch --depth 1
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN /bin/bash -c 'source $INSTALL_DIR/setupvars.sh && \
    accuracy_check -c sample/sample_config.yml -m data/test_models -s sample'

# Download DLI source code
WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark.git --depth 1 && \
    pip3 install docker PyYAML
