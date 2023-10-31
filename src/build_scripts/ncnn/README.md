# ncnn build and configure for Linux

## ncnn build and configure using scripts

Build and install prerequisites for ncnn build:
```bash
# Into dl-benchmark/src/ncnn/build directory:
sudo ./build_prerequisites_linux_x86_64.sh
```

Build and install ncnn:
```bash
# Into dl-benchmark/src/ncnn/build directory:
sudo ./build_ncnn_linux_x86_64.sh
```

## Manual ncnn build and configure

### 1. Install prerequisites

#### 1.1 Packages

Update and install required packages:
```bash
sudo apt update
sudo apt install build-essential git cmake libprotobuf-dev protobuf-compiler libvulkan-dev libopencv-dev vulcan-tools autoconf automake libtool curl make g++ unzip
```

#### 1.2 Protobuf

##### 1.2.1 Clone protobuf repo:
```bash
git clone https://github.com/protocolbuffers/protobuf.git -b v4.24.4
```

##### 1.2.2 Update submodules:
```bash
cd protobuf && git submodule update --init --recursive
```

##### 1.2.3 Build protobuf:
```bash
cmake . -DCMAKE_CXX_STANDARD=14
cmake --build . --parallel $(nproc)
```

##### 1.2.4 Run tests:
```bash
ctest --verbose
```

##### 1.2.5 Install built package:
```bash
sudo cmake --install .
```

#### 1.3 OpenCV

##### 1.3.1 Download OpenCV release:
```bash
wget https://github.com/opencv/opencv/archive/4.8.0.zip && unzip opencv-4.8.0.zip && cd opencv-4.8.0/
```

##### 1.3.2 Make build directory:
```bash
mkdir build && cd build
```

##### 1.3.3 Build OpenCV:
```bash
sudo cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
sudo make -j$(nproc)
```

##### 1.3.4 Install built OpenCV:
```bash
sudo make install
```

##### 1.3.5 Update library links configuration by adding path to OpenCV installation:
```bash
echo "include /usr/local/lib" | sudo tee -a /etc/ld.so.conf
sudo ldconfig
```

##### 1.3.6 Modify ```bashrc``` file:
```bash
printf "PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig\nexport PKG_CONFIG_PATH" | sudo tee -a /etc/bash.bashrc
```

### 2. Install ncnn

##### 2.1 Clone ncnn repo:
```bash
git clone https://github.com/Tencent/ncnn.git
```

##### 2.2 Update submodules:
```bash
cd ncnn && git submodule update --init
```

##### 2.3 Make build directory:
```bash
mkdir build && cd build
```

##### 2.4 Build ncnn:
```bash
cmake -DCMAKE_BUILD_TYPE=Release -DNCNN_VULKAN=ON -DNCNN_SYSTEM_GLSLANG=ON -DNCNN_BUILD_EXAMPLES=ON ..
make -j$(nproc)
```

##### 2.5 Install ncnn:
```bash
make install
```

##### 2.6 Make directory for ncnn binaries:
```bash
sudo mkdir /usr/local/lib/ncnn
```

##### 2.7 Copy ncnn binaries:
```bash
sudo cp -r install/include/ncnn /usr/local/include/ncnn && sudo cp -r install/lib/libncnn.a /usr/local/lib/ncnn/libncnn.a
```

### 3. Verification steps

##### 3.1 Run examlpes:
```bash
# Into ./ncnn/build directory:
cd ../examples && ../build/examples/squeezenet ../images/256-ncnn.png
```

##### 3.2 Run benchmarks:
```bash
# Into ./ncnn/build directory:
cd ../bechmark && ../build/benchmark/benchncnn 10 $(nproc) 0 0
```
