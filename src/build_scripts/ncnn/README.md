# ncnn build and configure using scripts

```bash
# Into dl-benchmark/src/ncnn/build directory:
sudo ./build_prerequisites_linux_x86_64.sh
```

```bash
# Into dl-benchmark/src/ncnn/build directory:
sudo ./build_ncnn_linux_x86_64.sh
```

# Manual ncnn build and configure

### 1. Install prerequisites

#### 1.1 Packages
```bash
sudo apt update
```

```bash
sudo apt install build-essential git cmake libprotobuf-dev protobuf-compiler libvulkan-dev libopencv-dev vulcan-tools autoconf automake libtool curl make g++ unzip
```

#### 1.2 Protobuf

```bash
git clone https://github.com/protocolbuffers/protobuf.git -b v4.24.4
```

```bash
cd protobuf && git submodule update --init --recursive
```

```bash
cmake . -DCMAKE_CXX_STANDARD=14
```

```bash
cmake --build . --parallel 8
```

```bash
ctest --verbose
```

```bash
sudo cmake --install .
```

#### 1.3 OpenCV

```bash
wget https://github.com/opencv/opencv/archive/4.8.0.zip && unzip opencv-4.8.0.zip && cd opencv-4.8.0/
```

```bash
mkdir build && cd build
```

```bash
sudo cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
```

```bash
sudo make -j8
```

```bash
sudo make install
```

```bash
echo "include /usr/local/lib" | sudo tee -a /etc/ld.so.conf
```

```bash
sudo ldconfig
```

```bash
printf "PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig\nexport PKG_CONFIG_PATH" | sudo tee -a /etc/bash.bashrc
```

### 2. Install ncnn

```bash
git clone https://github.com/Tencent/ncnn.git
```

```bash
cd ncnn && git submodule update --init
```

```bash
mkdir build && cd build
```

```bash
cmake -DCMAKE_BUILD_TYPE=Release -DNCNN_VULKAN=ON -DNCNN_SYSTEM_GLSLANG=ON -DNCNN_BUILD_EXAMPLES=ON ..
```

```bash
make -j8
```

```bash
make install
```

```bash
sudo mkdir /usr/local/lib/ncnn
```

```bash
sudo cp -r install/include/ncnn /usr/local/include/ncnn && sudo cp -r install/lib/libncnn.a /usr/local/lib/ncnn/libncnn.a
```

### 3. Verification steps

```bash
# Into ./ncnn/build directory:
cd ../examples && ../build/examples/squeezenet ../images/256-ncnn.png
```

```bash
# Into ./ncnn/build directory:
cd ../bechmark && ../build/benchmark/benchncnn 10 $(nproc) 0 0
```
