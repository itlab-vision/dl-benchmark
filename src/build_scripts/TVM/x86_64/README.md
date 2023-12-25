# Build TVM on x86

First you need to install llvm, if they are not installed

```bash
sudo apt update && sudo apt upgrade
sudo apt install gcc g++ llvm cmake
```

We used anaconda3 to run it. We have created separate dependencies for Python 3.8

```bash
conda create --no-default-packages -n tvm_src -y python=3.8
conda activate tvm_src
```

Installing additional libraries to run benchmarking
```bash
pip install numpy opencv-python scipy
```

Installing additional libraries for building TVM
```bash
conda install -c conda-forge -y gcc=12.1.0
conda install -c conda-forge -y gxx_linux-64

pip install traitlets==5.9.0 decorator attrs typing-extensions psutil scipy pybind11 
```

Downloading and building apache-tvm or you can run ```./build_tvm_x86.sh <tvm_dir>```
```bash
git clone --recursive https://github.com/apache/tvm tvm
cd tvm
mkdir build
cd build

cmake -DUSE_LLVM=ON ..
make -j

cd ../python
python setup.py install --user
```

