# Build TVM on x86

1. First you need to install llvm, if it is not installed.

   ```bash
   sudo apt update && sudo apt upgrade
   sudo apt install gcc g++ llvm cmake
   ```

1. We used Anaconda3 to run TVM. We have created separate virtual environment for Python 3.8.

   ```bash
   conda create --no-default-packages -n tvm_src -y python=3.8
   conda activate tvm_src
   ```

1. Installing additional libraries to run the DLI benchmark.

   ```bash
   pip install numpy opencv-python scipy
   ```

1. Installing additional libraries for building TVM.

   ```bash
   conda install -c conda-forge -y gcc=12.1.0
   conda install -c conda-forge -y gxx_linux-64

   pip install traitlets==5.9.0 decorator attrs typing-extensions psutil scipy pybind11 
   ```

1. Downloading and building Apache TVM or you can run ```./build_tvm_x86.sh <tvm_dir>```.

   ```bash
   git clone --recursive https://github.com/apache/tvm -b v0.15.0 tvm
   cd tvm

   git apply <path>/fix_relay_init_0.15.diff
   
   mkdir build
   cd build

   cmake -DUSE_LLVM=ON ..
   make -j

   cd ../python
   python setup.py install --user
   ```

