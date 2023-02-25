FROM ubuntu:18.04
USER root
WORKDIR /
RUN useradd -ms /bin/bash openvino && \
    chown openvino -R /home/openvino
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
                  python-pip \
                  python3-pip \
                  python3-setuptools \
                  python3-dev \
                  python3-venv \
                  pciutils \
                  libpython3.7 \
                  udev \
                  unzip \
                  wget \
                  git"
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

#install openvino
RUN wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB && \
    sudo apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB
RUN echo "deb https://apt.repos.intel.com/openvino/2022 bionic main" | sudo tee /etc/apt/sources.list.d/intel-openvino-2022.list && \
    sudo apt update && echo y | sudo apt install openvino-2022.1.0 openvino-opencv

#install openvino dependencies
ENV INSTALL_DIR /opt/intel/openvino_2022
WORKDIR $INSTALL_DIR/install_dependencies
RUN echo y | ./install_openvino_dependencies.sh
RUN cat /root/.bashrc > tmp && echo 'source $INSTALL_DIR/setupvars.sh' > /root/.bashrc

#configurations for GPU, MYRIAD
RUN echo y | ./install_NEO_OCL_driver.sh
RUN usermod -a -G video,users root

#openvino-dev
WORKDIR /tmp/
RUN pip3 install --upgrade pip && \
    pip3 install openvino-dev==2022.1

#accuracy-check
RUN git clone --recursive https://github.com/openvinotoolkit/open_model_zoo.git --branch 2022.1.0 --single-branch
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN pip3 uninstall opencv-python -y && pip3 install "opencv-python-headless<4.7"
RUN /bin/bash -c "accuracy_check -c sample/sample_config.yml -m data/test_models -s sample"

#DLB
WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark.git && \
    pip3 install docker PyYAML

#DLB dataset
ARG DATASET_DOWNLOAD_LINK=<Link to dataset project>
RUN git clone $DATASET_DOWNLOAD_LINK
