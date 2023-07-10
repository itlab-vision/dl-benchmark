FROM ubuntu_for_dli

# Install OpenVINO
ENV INSTALL_DIR /opt/intel/openvino_2022
ARG OV_SHORT_VERSION=2022.3.1
ARG OV_LONG_VERSION="${OV_SHORT_VERSION}.9227.cf2c7da5689_x86_64"
RUN sudo mkdir /opt/intel && \
    wget https://storage.openvinotoolkit.org/repositories/openvino/packages/${OV_SHORT_VERSION}/linux/l_openvino_toolkit_ubuntu20_${OV_LONG_VERSION}.tgz \
        -O /tmp/openvino.tgz --no-check-certificate --quiet && \
    tar -zxvf /tmp/openvino.tgz -C /opt/intel/ && \
    sudo ln -s /opt/intel/l_openvino_toolkit_ubuntu20_${OV_LONG_VERSION} $INSTALL_DIR && \
    rm /tmp/openvino.tgz

# Install OpenVINO dependencies
WORKDIR $INSTALL_DIR/install_dependencies
RUN ls -la $INSTALL_DIR/install_dependencies && echo y | ./install_openvino_dependencies.sh
RUN cat /root/.bashrc > tmp && echo 'source $INSTALL_DIR/setupvars.sh' > /root/.bashrc

# Configure for GPU, MYRIAD
RUN echo y | ./install_NEO_OCL_driver.sh
RUN usermod -a -G video,users root

# Install OpenCV
WORKDIR /tmp/
ARG OCV_VERSION=4.7.0
RUN pip uninstall opencv-python -y
RUN git clone --recurse-submodules https://github.com/opencv/opencv.git  --depth 1 --branch ${OCV_VERSION} --single-branch
ENV OpenCV_BUILD_DIR=/tmp/build-opencv
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
        rm -r /tmp/opencv
ENV OpenCV_INSTALL_DIR="$OpenCV_BUILD_DIR/install"
ENV OpenCV_DIR="$OpenCV_INSTALL_DIR/cmake"
ENV LD_LIBRARY_PATH="$OpenCV_INSTALL_DIR/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
ENV PYTHONPATH="$OpenCV_INSTALL_DIR/python/python3/cv2/python-3.8${PYTHONPATH:+:$PYTHONPATH}"

#accuracy-check
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
RUN wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
RUN tar xvf cifar-10-python.tar.gz -C sample
RUN /bin/bash -c 'source $INSTALL_DIR/setupvars.sh && \
    accuracy_check -c sample/sample_config.yml -m data/test_models -s sample'

# Download dataset if repository with dataset is set
ARG DATASET_DOWNLOAD_LINK
RUN if [ -z "$DATASET_DOWNLOAD_LINK" ] ; then echo Argument DATASET_DOWNLOAD_LINK not provided ; else git clone $DATASET_DOWNLOAD_LINK ; fi
WORKDIR /tmp/
