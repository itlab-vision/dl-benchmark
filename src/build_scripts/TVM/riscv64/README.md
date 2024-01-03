# Build TVM Runtime on RISC-V

We used system Python 3.11.

1. Creating virtual environment.

    ```bash
    python3.11 -m venv <venv_dir>/py_venv/tvm_venv
    source <venv_dir>/py_venv/tvm_venv/bin/activate
    ```

1. Installing additional libraries.

    ```bash
    pip install -U pip setuptools
    pip install six wheel numpy
    ```

1. Downloading and building Apache TVM runtime or you can run ```./build_tvm_risc-v.sh <tvm_dir>```.

    ```bash
    git clone --recursive https://github.com/apache/tvm
    cd tvm 
    mkdir build
    cd build
    cmake -DCMAKE_SYSTEM_NAME=Linux \
          -DCMAKE_SYSTEM_VERSION=1 \
          -DCMAKE_C_COMPILER=gcc \
          -DCMAKE_CXX_COMPILER=g++ \
          ..
    make runtime -j

    cd ../..
    ```

1. Downloading and building OpenCV or you can run ```./build_opencv_risc-v.sh <opencv_dir>```.

    ```bash
    git clone --depth 1 https://github.com/opencv/opencv/
    cd opencv 
    mkdir build
    cd build
    cmake -G "Unix Makefiles" \
          -DCMAKE_INSTALL_PREFIX=../opencv_install \
          -DCMAKE_BUILD_TYPE=Release \
          -DBUILD_LIST=core,imgcodecs,python3 \
          -DBUILD_opencv_python3=ON \
          -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
          -DBUILD_NEW_PYTHON_SUPPORT=ON \
          ..
    make -j
    make install
    ```

1. Before using the DLI benchmark, activate virtual environment and set paths for the Apache TVM and OpenCV libraries.

    ```bash
    source <venv_dir>/py_venv/tvm_venv/bin/activate
    source <opencv_dir>/opencv/opencv_install/bin/setup_vars_opencv4.sh

    export TVM_HOME=<tvm_dir>/tvm/
    export PYTHONPATH=$TVM_HOME/python:${PYTHONPATH}
    ```
    
**Note:** running ```make``` on risc-v with ```-j``` may cause problems, in which case it is recommended to set up ```-jn```,
specifying the number of cores less than the number of physical cores.
