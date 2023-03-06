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
                  git"
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

# Install OpenVINO
RUN sudo mkdir /opt/intel && \
    curl -L https://storage.openvinotoolkit.org/repositories/openvino/packages/2022.2/linux/l_openvino_toolkit_ubuntu20_2022.2.0.7713.af16ea1d79a_x86_64.tgz --output openvino_2022.2.0.7713.tgz && \
    tar -xf openvino_2022.2.0.7713.tgz && \
    sudo mv l_openvino_toolkit_ubuntu20_2022.2.0.7713.af16ea1d79a_x86_64 /opt/intel/openvino_2022.2.0.7713 && \
    sudo ln -s /opt/intel/openvino_2022.2.0.7713 /opt/intel/openvino_2022

RUN tar -xf openvino_2022.2.0.7713.tgz && \ 
    ls -laR l_openvino_toolkit_ubuntu20_2022.2.0.7713.af16ea1d79a_x86_64/install_dependencies

RUN ls /opt/intel/openvino_2022/

# Install OpenVINO dependencies
ENV INSTALL_DIR /opt/intel/openvino_2022/
WORKDIR $INSTALL_DIR/install_dependencies
RUN ls -la /opt/intel/openvino_2022/install_dependencies && echo y | ./install_openvino_dependencies.sh
RUN cat /root/.bashrc > tmp && echo 'source $INSTALL_DIR/setupvars.sh' > /root/.bashrc

# Configure for GPU, MYRIAD
RUN echo y | ./install_NEO_OCL_driver.sh
RUN usermod -a -G video,users root

# Install openvino-dev
WORKDIR /tmp/
RUN pip3 install --upgrade pip
RUN pip3 install openvino-dev==2022.2

# Test Accuracy Checker
RUN git clone --recursive https://github.com/openvinotoolkit/open_model_zoo.git --branch 2022.2.0 --single-branch --depth 1
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN pip3 uninstall opencv-python -y && pip3 install "opencv-python-headless"
RUN /bin/bash -c "accuracy_check -c sample/sample_config.yml -m data/test_models -s sample"

# Download DLI dource code
WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark.git --depth 1 && \
    pip3 install docker PyYAML

# Download dataset
ARG DATASET_DOWNLOAD_LINK=<Link to dataset project>
RUN git clone $DATASET_DOWNLOAD_LINK
