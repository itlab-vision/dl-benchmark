cd $1

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
      
make -j2
make install

