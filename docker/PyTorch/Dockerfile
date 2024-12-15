FROM ubuntu_for_dli

WORKDIR /root/

ARG TORCH_VERSION=2.0.1
ARG TORCHVISION_VERSION=0.15.2
ARG OCV_VERSION=4.7.0
ARG CMAKE_VERSION=3.24

# Install cmake
WORKDIR /tmp/
RUN pip3 install --upgrade pip
RUN pip3 install cmake==${CMAKE_VERSION}

# Install OpenCV using C++ build
WORKDIR /tmp/
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

# Install PyTorch using C++ build
WORKDIR /tmp/
RUN git clone --recurse-submodules https://github.com/pytorch/pytorch  --depth 1 --branch v${TORCH_VERSION} --single-branch
RUN pip3 install -r ./pytorch/requirements.txt
ENV TORCH_BUILD_DIR=/tmp/build-torch
RUN mkdir $TORCH_BUILD_DIR
WORKDIR $TORCH_BUILD_DIR
RUN cmake \
        -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DPYTHON_EXECUTABLE=`which python3` \
        -DCMAKE_INSTALL_PREFIX=install \
        /tmp/pytorch && cmake --build . --target install -- -j$(nproc --all) && rm -r /tmp/pytorch
ENV TORCH_INSTALL_DIR="$TORCH_BUILD_DIR/install"

# Install PyTorch Python
RUN pip3 install torch==${TORCH_VERSION} \
                 torchvision==${TORCHVISION_VERSION}

# Build Benchmark C++
WORKDIR /tmp/
RUN cd dl-benchmark && git submodule update --init && cd ..
RUN mkdir benchmark_build && cd benchmark_build && \
    cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_PYTORCH_LAUNCHER=ON \
        -DTorch_DIR="$TORCH_INSTALL_DIR/share/cmake/Torch/" \
        /tmp/dl-benchmark/src/cpp_dl_benchmark && cmake --build . -- -j$(nproc --all)

# Install Accuracy Checker
ENV ACCURACY_CHECKER_PATH=/tmp/open_model_zoo/tools/accuracy_checker
WORKDIR $ACCURACY_CHECKER_PATH
COPY config.yml config.yml
# make module path relative in config
ARG MODELS_DIR=$ACCURACY_CHECKER_PATH/data/test_models
RUN sed -i 's|MODELS_DIR|'${MODELS_DIR}'|g' config.yml

RUN python3 setup.py install_core; \
    accuracy_check -c config.yml -m data/test_models -s sample

WORKDIR /tmp/
