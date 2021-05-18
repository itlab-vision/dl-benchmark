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
                  libpython3.6 \
                  udev \
                  unzip \
                  wget \
                  git"
RUN apt-get update && \
    apt-get install -y -qq --no-install-recommends ${DEPENDENCIES} && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install lxml PyYAML requests numpy networkx==2.3 defusedxml

ARG DOWNLOAD_LINK=<Link to download OpenVINO>
WORKDIR /tmp
ENV INSTALL_DIR /opt/intel/openvino
RUN curl -LOJ "${DOWNLOAD_LINK}" && \
    tar -xzf ./*.tgz && \
    cd l_openvino_toolkit* && \
    sed -i 's/decline/accept/g' silent.cfg && \
    ./install.sh -s silent.cfg && \
    rm -rf /tmp/*

#install openvino dependencies
WORKDIR $INSTALL_DIR/install_dependencies
RUN echo y | ./install_openvino_dependencies.sh
RUN echo y | ./install_NEO_OCL_driver.sh
RUN usermod -a -G video root

#install additional openvino dependencies
WORKDIR $INSTALL_DIR/deployment_tools/demo
RUN echo y | ./demo_security_barrier_camera.sh || exit 0
RUN echo y | ./demo_security_barrier_camera -d GPU || exit 0

#install model_optimizer dependencies
WORKDIR $INSTALL_DIR/deployment_tools/model_optimizer/install_prerequisites
RUN echo y | ./install_prerequisites.sh

WORKDIR $INSTALL_DIR/deployment_tools/tools/model_downloader/
RUN python3 downloader.py --all
RUN python3 converter.py --all --mo $INSTALL_DIR/deployment_tools/model_optimizer/mo.py || exit 0

WORKDIR /tmp/
RUN git clone https://github.com/itlab-vision/dl-benchmark.git

ARG DATASET_DOWNLOAD_LINK=<Link to dataset project>
RUN git clone $DATASET_DOWNLOAD_LINK

#create python environment for accuracy checker
WORKDIR /opt/intel
RUN mkdir accuracy_checker_env && \
    python3 -m virtualenv -p /usr/bin/python3 ./accuracy_checker_env
RUN echo 'source ./accuracy_checker_env/bin/activate' && \
    pip install opencv-python pyaml docker

#install accuracy_checker
WORKDIR $INSTALL_DIR/deployment_tools/open_model_zoo/tools/accuracy_checker
RUN python3 setup.py install_core
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN /bin/bash -c "source $INSTALL_DIR//bin/setupvars.sh && \
    export MO_DIR=$INSTALL_DIR/deployment_tools/model_optimizer && \
    accuracy_check -c sample/sample_config.yml -m data/test_models -s sample"
	
WORKDIR /tmp/
RUN cat /root/.bashrc > tmp && echo 'source $INSTALL_DIR/bin/setupvars.sh' > /root/.bashrc && \
    echo 'export MO_DIR=$INSTALL_DIR/deployment_tools/model_optimizer' >> /root/.bashrc && \
    cat tmp >> /root/.bashrc && rm tmp
