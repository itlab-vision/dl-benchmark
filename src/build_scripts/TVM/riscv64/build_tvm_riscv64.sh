cd $1

git clone --recursive https://github.com/apache/tvm tvm
cd tvm 
mkdir build
cd build
cmake -DCMAKE_SYSTEM_NAME=Linux \
      -DCMAKE_SYSTEM_VERSION=1 \
      -DCMAKE_C_COMPILER=gcc \
      -DCMAKE_CXX_COMPILER=g++ \
      ..

make runtime -j

