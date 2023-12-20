#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
REPO_ROOT=$(realpath "$SCRIPT_DIR/../../..")
git submodule update --init --recursive

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
    --rebuild_cpp_launcher)
      REBUILD_CPP_LAUNCHER=YES
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
    --rebuild_cpp_launcher - Rebuild cpp tflite launcher
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

if [ ! -d ${BUILD_DIR}/tflite_riscv_build ]
then
    echo "Builded TFLite not exist in ${BUILD_DIR}. Build it using build_prerequisites_linux_riscv.sh"
    exit 1
else
    TFLITE_RISCV_BUILD=${BUILD_DIR}/tflite_riscv_build
    echo "TFLITE_RISCV_BUILD_DIR = ${TFLITE_RISCV_BUILD}"
fi

if [ ! -d ${BUILD_DIR}/opencv_riscv_build ]
then
    echo "Builded OpenCV not exist in ${BUILD_DIR}. Build it using build_prerequisites_linux_riscv.sh"
    exit 1
else
    OPENCV_RISCV_BUILD=${BUILD_DIR}/opencv_riscv_build
    echo "OPENCV_RISCV_BUILD_DIR = ${OPENCV_RISCV_BUILD}"
fi

if [ ! -d ${WORKDIR}/tensorflow ]
then
    echo "Tensorflow sources not exist in ${WORKDIR}. Download it using build_prerequisites_linux_riscv.sh"
    exit 1
else
    TFLITE_SRC_DIR=${WORKDIR}/tensorflow
    echo "TFLITE_SRC_DIR = ${TFLITE_SRC_DIR}"
fi

if [ ! -d ${BUILD_DIR}/json_build ]
then
    echo "Builded JSON not exist in ${BUILD_DIR}. Build it using build_prerequisites_linux_riscv.sh"
    exit 1
else
    JSON_BUILD=${BUILD_DIR}/json_build
    echo "JSON_BUILD_DIR = ${JSON_BUILD}"
fi

if [ ! -d ${WORKDIR}/json ]
then
    git clone https://github.com/nlohmann/json.git ${WORKDIR}/json
fi
export CPATH=${WORKDIR}/json/include:$CPATH

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


if [ -d ${BUILD_DIR}/cpp_tflite_launcher_riscv_build ]
then
    if [[ ! -z "${REBUILD_CPP_LAUNCHER}" ]]
    then
        rm -rf ${BUILD_DIR}/cpp_tflite_launcher_riscv_build/*
    fi
else
    mkdir ${BUILD_DIR}/cpp_tflite_launcher_riscv_build
    REBUILD_CPP_LAUNCHER=YES
fi

if [[ ! -z "${REBUILD_CPP_LAUNCHER}" ]]
then
    cmake -S ${REPO_ROOT}/src/cpp_dl_benchmark \
        -B ${BUILD_DIR}/cpp_tflite_launcher_riscv_build -D CMAKE_BUILD_TYPE=Release -D ENABLE_CLANG_FORMAT=OFF \
        -D CMAKE_SYSTEM_NAME=Linux -D CMAKE_SYSTEM_PROCESSOR=riscv64 -D BUILD_SHARED_LIBS=OFF -D CMAKE_SYSROOT=${RISCV_SYSROOT} \
        -D CMAKE_C_COMPILER=${RISCV_C_COMPILER} -D CMAKE_CXX_COMPILER=${RISCV_CXX_COMPILER} -D CMAKE_FIND_ROOT_PATH_MODE_PROGRAM=NEVER \
        -D CMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY -D CMAKE_FIND_ROOT_PATH_MODE_INCLUDE=BOTH -D CMAKE_FIND_ROOT_PATH_MODE_PACKAGE=ONLY \
        -D CMAKE_CXX_FLAGS_INIT="-march=rv64imafdc -mabi=lp64d" -D CMAKE_C_FLAGS_INIT="-march=rv64imafdc -mabi=lp64d" \
        -D BUILD_TFLITE_LAUNCHER=ON -D BUILD_TFLITE_XNNPACK_LAUNCHER=ON -D nlohmann_json_DIR=${JSON_BUILD} \
        -D CMAKE_FIND_ROOT_PATH=${TFLITE_RISCV_BUILD} \
        -D TENSORFLOW_SRC_DIR=${TFLITE_SRC_DIR} -D TFLITE_BUILD_DIR=${TFLITE_RISCV_BUILD} -D OpenCV_DIR=${OPENCV_RISCV_BUILD}
    cmake --build ${BUILD_DIR}/cpp_tflite_launcher_riscv_build --config Release -- -j$(nproc)
fi

rm -rf ${BUILD_DIR}/riscv64_send_archive/*
cp -r ${TOOLCHAIN_PATH}/sysroot ${BUILD_DIR}/riscv64_send_archive/
cp -r ${BUILD_DIR}/cpp_tflite_launcher_riscv_build ${BUILD_DIR}/riscv64_send_archive
cp -r ${TFLITE_RISCV_BUILD} ${BUILD_DIR}/riscv64_send_archive
cp -r ${OPENCV_RISCV_BUILD} ${BUILD_DIR}/riscv64_send_archive
tar -cvzf ${BUILD_DIR}/riscv64_send_archive.tgz -C ${BUILD_DIR}/riscv64_send_archive .
