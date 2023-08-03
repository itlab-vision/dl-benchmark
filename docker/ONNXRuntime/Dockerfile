FROM ubuntu_for_dli

#install cmake
WORKDIR /tmp/
RUN pip3 install --upgrade pip
ARG CMAKE_VERSION=3.24
RUN pip3 install cmake==${CMAKE_VERSION}

# Install OpenCV
ARG OCV_VERSION=4.7.0
RUN pip uninstall opencv-python -y
RUN git clone --recurse-submodules https://github.com/opencv/opencv.git  --depth 1 --branch ${OCV_VERSION} --single-branch
ENV OpenCV_BUILD_DIR=/tmp/build-opencv
RUN mkdir $OpenCV_BUILD_DIR
WORKDIR $OpenCV_BUILD_DIR
RUN /bin/bash -c 'cmake -G Ninja \
        -D CMAKE_INSTALL_PREFIX=install \
        -D CMAKE_BUILD_TYPE=Release \
        -D BUILD_EXAMPLES=OFF \
        -D BUILD_TESTS=OFF \
        -D BUILD_DOCS=OFF \
        -D OPENCV_LIB_INSTALL_PATH=lib \
        -D OPENCV_CONFIG_INSTALL_PATH=cmake \
        -D PYTHON3_PACKAGES_PATH=install/python/python3 \
        /tmp/opencv/ && ninja && cmake --install .' && \
        rm -r /tmp/opencv
ENV OpenCV_INSTALL_DIR="$OpenCV_BUILD_DIR/install"
ENV OpenCV_DIR="$OpenCV_INSTALL_DIR/cmake"
ENV LD_LIBRARY_PATH="$OpenCV_INSTALL_DIR/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
ENV PYTHONPATH="$OpenCV_INSTALL_DIR/python/python3/cv2/python-3.8${PYTHONPATH:+:$PYTHONPATH}"

# Install onnxruntime
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
RUN pip install onnxruntime==${ONNX_VERSION} && pip install onnx==${ONNX_VERSION}

# accuracy-check
WORKDIR /tmp/open_model_zoo/tools/accuracy_checker
COPY config.yml config.yml
RUN accuracy_check -c config.yml -m data/test_models -s sample
RUN rm config.yml

WORKDIR /tmp/
