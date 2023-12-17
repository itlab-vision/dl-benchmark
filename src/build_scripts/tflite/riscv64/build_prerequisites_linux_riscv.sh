#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
REPO_ROOT=$(realpath "$SCRIPT_DIR/../../..")

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -t|--toolchain_path)
      TOOLCHAIN_PATH="$2"
      shift # past argument
      shift # past value
      ;;
    -w|--workdir)
      WORKDIR="$2"
      shift # past argument
      shift # past value
      ;;
    -b|--build_dir)
      BUILD_DIR="$2"
      shift # past argument
      shift # past value
      ;;
    --rebuild_tflite)
      REBUILD_TFLITE=YES
      shift # past argument
      shift # past value
      ;;
    --rebuild_opencv)
      REBUILD_OPENCV=YES
      shift # past argument
      shift # past value
      ;;
    --rebuild_json)
      REBUILD_JSON=YES
      shift # past argument
      shift # past value
      ;;
    -h|--help)
      PRINT_HELP=YES
      shift # past argument
      shift # past value
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters
if [[ ! -z "${PRINT_HELP}" ]] 
then
    echo "Supported arguments: 
    -t / --tolchain_path - path to RISCV gcc toolchain. If not specified, the toolchain will be downloaded to workdir
    -w / --workdir - working directory for downloading and building processes. Default: dl-benchmark/downloads
    -b / --build_dir - directory for builded packages. Default: dl-benchmark/build
    --rebuild_tflite - Rebuild tflite framework
    --rebuild_opencv - Rebuild opencv framework
    --rebuild_json - Rebuild json framework
    "
    exit 1
fi

if [[ -z "${WORKDIR}" ]] 
then
    WORKDIR="${REPO_ROOT}/downloads"
    if [[ ! -d ${WORKDIR} ]]
    then
        mkdir ${WORKDIR}
    fi
fi

echo "WORKDIR = ${WORKDIR}"

if [[ -z "${BUILD_DIR}" ]] 
then
    BUILD_DIR="${REPO_ROOT}/build"
    if [[ ! -d ${BUILD_DIR} ]]
    then
        mkdir ${BUILD_DIR}
    fi
fi

echo "BUILD_DIR = ${BUILD_DIR}"

if [[ -z "${TOOLCHAIN_PATH}" ]] 
then
    if [ ! -d ${WORKDIR}/riscv ]
    then
        echo "Starting downloading riscv-gnu-toolchain for ubuntu 20.04 version 2023.11.17..."
        wget -O ${WORKDIR}/riscv_toolchain.tgz 'https://github.com/riscv-collab/riscv-gnu-toolchain/releases/download/2023.11.17/riscv64-glibc-ubuntu-20.04-gcc-nightly-2023.11.17-nightly.tar.gz' 
        tar -xvzf ${WORKDIR}/riscv_toolchain.tgz -C ${WORKDIR}
    fi
    TOOLCHAIN_PATH=${WORKDIR}/riscv
fi

if [ ! -d ${TOOLCHAIN_PATH}/bin ] && [ ! -d ${TOOLCHAIN_PATH}/sysroot ] && \
      [ ! -f ${TOOLCHAIN_PATH}/bin/riscv64-unknown-linux-gnu-gcc ] && \
      [ ! -f ${TOOLCHAIN_PATH}/bin/riscv64-unknown-linux-gnu-g++ ]
then
    echo "Error: Not suitable toolchain in TOOLCHAIN_PATH. Toolchain must contain riscv64-unknown-linux-gnu-gcc and riscv64-unknown-linux-gnu-g++ compilers"
    exit 1
else
    echo "TOOLCHAIN_PATH = ${TOOLCHAIN_PATH}"
    RISCV_C_COMPILER=${TOOLCHAIN_PATH}/bin/riscv64-unknown-linux-gnu-gcc
    RISCV_CXX_COMPILER=${TOOLCHAIN_PATH}/bin/riscv64-unknown-linux-gnu-g++
    RISCV_SYSROOT=${TOOLCHAIN_PATH}/sysroot
fi

if [ ! -d ${WORKDIR}/tensorflow ]
then
    git clone https://github.com/tensorflow/tensorflow ${WORKDIR}/tensorflow
    cd ${WORKDIR}/tensorflow
    git checkout v2.14.0
fi

if [ -d ${BUILD_DIR}/tflite_riscv_build ]
then
    if [[ ! -z "${REBUILD_TFLITE}" ]]
    then
        rm -rf ${BUILD_DIR}/tflite_riscv_build/*
    fi
else
    mkdir ${BUILD_DIR}/tflite_riscv_build
    REBUILD_TFLITE=YES
fi

if [[ ! -z "${REBUILD_TFLITE}" ]]
then
    echo "Start building TFLite for RISCV..."
    cmake -S ${WORKDIR}/tensorflow/tensorflow/lite/ -B ${BUILD_DIR}/tflite_riscv_build -D CMAKE_BUILD_TYPE=Release -D BUILD_SHARED_LIBS=ON \
        -D TFLITE_ENABLE_GPU=ON -D CMAKE_SYSTEM_NAME=Linux -D CMAKE_SYSTEM_PROCESSOR=riscv64 \
        -D CMAKE_C_COMPILER=${RISCV_C_COMPILER} -D CMAKE_CXX_COMPILER=${RISCV_CXX_COMPILER} -D CMAKE_FIND_ROOT_PATH_MODE_PROGRAM=NEVER \
        -D CMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY -D CMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY -D CMAKE_FIND_ROOT_PATH_MODE_PACKAGE=ONLY \
        -D CMAKE_CXX_FLAGS_INIT="-march=rv64imafdc -mabi=lp64d" -D CMAKE_C_FLAGS_INIT="-march=rv64imafdc -mabi=lp64d"

    cmake --build ${BUILD_DIR}/tflite_riscv_build --config Release --parallel $(nproc)

    mkdir ${BUILD_DIR}/tmp_tflite_riscv_build_libs
    find ${BUILD_DIR}/tflite_riscv_build -type f -name "*.so" -exec cp {} ${BUILD_DIR}/tmp_tflite_riscv_build_libs \;
    cp ${BUILD_DIR}/tmp_tflite_riscv_build_libs/* ${BUILD_DIR}/tflite_riscv_build
    rm -rf ${BUILD_DIR}/tmp_tflite_riscv_build_libs/
fi

if [ ! -d ${WORKDIR}/opencv ]
then
    git clone https://github.com/opencv/opencv.git ${WORKDIR}/opencv
fi

if [ -d ${BUILD_DIR}/opencv_riscv_build ]
then
    if [[ ! -z "${REBUILD_OPENCV}" ]]
    then
        rm -rf ${BUILD_DIR}/opencv_riscv_build/*
    fi
else
    mkdir ${BUILD_DIR}/opencv_riscv_build
    REBUILD_OPENCV=YES
fi

if [[ ! -z "${REBUILD_OPENCV}" ]]
then
    echo "Start building OpenCV for RISCV..."
    cmake -S ${WORKDIR}/opencv -B ${BUILD_DIR}/opencv_riscv_build -D CMAKE_BUILD_TYPE=Release \
        -D CMAKE_SYSTEM_NAME=Linux -D CMAKE_SYSTEM_PROCESSOR=riscv64 -D BUILD_SHARED_LIBS=OFF -D CMAKE_SYSROOT=${RISCV_SYSROOT} \
        -D CMAKE_C_COMPILER=${RISCV_C_COMPILER} -D CMAKE_CXX_COMPILER=${RISCV_CXX_COMPILER} -D CMAKE_FIND_ROOT_PATH_MODE_PROGRAM=NEVER \
        -D CMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY -D CMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY -D CMAKE_FIND_ROOT_PATH_MODE_PACKAGE=ONLY \
        -D BUILD_TESTS=OFF -D BUILD_EXAMPLES=OFF -D BUILD_PERF_TESTS=OFF \
        -D CMAKE_CXX_FLAGS_INIT="-march=rv64imafdc -mabi=lp64d" -D CMAKE_C_FLAGS_INIT="-march=rv64imafdc -mabi=lp64d"
    cd ${BUILD_DIR}/opencv_riscv_build
    make -j$(nproc)
fi

if [ ! -d ${WORKDIR}/json ]
then
    git clone https://github.com/nlohmann/json.git ${WORKDIR}/json
fi

if [ -d ${BUILD_DIR}/json_build ]
then
    if [[ ! -z "${REBUILD_JSON}" ]]
    then
        rm -rf ${BUILD_DIR}/json_build/*
    fi
else
    mkdir ${BUILD_DIR}/json_build
    REBUILD_JSON=YES
fi

if [[ ! -z "${REBUILD_JSON}" ]]
then
    echo "Start building JSON..."
    cmake -S ${WORKDIR}/json -B ${BUILD_DIR}/json_build -D JSON_BuildTests=OFF
    cmake --build ${BUILD_DIR}/json_build --config Release -- -j$(nproc)
fi

