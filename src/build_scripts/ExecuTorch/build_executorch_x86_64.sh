#!/bin/bash

# BUILD_DIR - directory for build ncnn
# INSTALL_PREFIX - directory for install ncnn

BUILD_DIR=${1:-""}
INSTALL_PREFIX=${2:-""}

if [ -z "$BUILD_DIR" ]; then
    echo "Error: Please set build directory as first argument"
    exit 1
fi

if [ -z "$INSTALL_PREFIX" ]; then
    echo "Error: Please set install prefix as second argument"
    exit 1
fi

echo "Creating build directory: ${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
cd "${BUILD_DIR}" || exit

echo "Creating conda environment"
conda create -y -n executorch_env python=3.10
conda activate executorch_env

echo "Clone repository"
git clone -b v0.5.0 https://github.com/pytorch/executorch
cd executorch && git submodule update --init

echo "Install requirements"
./install_requirements.sh

echo "Building and install ExecuTorch"
mkdir build1 && cd build1
cmake -DCMAKE_INSTALL_PREFIX="${INSTALL_PREFIX}" \
      -DEXECUTORCH_BUILD_EXTENSION_MODULE=ON \
      -DEXECUTORCH_BUILD_EXTENSION_RUNNER_UTIL=ON \
      -DEXECUTORCH_BUILD_EXTENSION_TENSOR=ON \
      -DEXECUTORCH_BUILD_DEVTOOLS=ON \
      -DBUILD_EXECUTORCH_PORTABLE_OPS=ON \
      -DEXECUTORCH_BUILD_XNNPACK=ON ../
make "-j$(nproc)"
make install

echo "Deactivating conda environment"
conda deactivate