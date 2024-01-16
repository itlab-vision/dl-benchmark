cd $1

git clone --recursive https://github.com/apache/tvm
cd tvm
mkdir build
cd build

cmake -DUSE_LLVM=ON ..
make -j

cd ../python
python setup.py install --user

