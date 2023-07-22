find_package(Torch REQUIRED)

file(GLOB_RECURSE HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/include/*")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*")

if (BUILD_PYTORCH_LAUNCHER)
    add_launcher(NAME pytorch_benchmark
                 SOURCES ${SOURCES}
                 HEADERS ${HEADERS}
                 INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
                 DEPENDENCIES ${TORCH_LIBRARIES}
                 DEFINITIONS PYTORCH)
endif()

if (BUILD_PYTORCH_TENSORRT_LAUNCHER)
    find_library(TORCH_TENSORRT_LIB libtorchtrt.so
                 ${TORCH_TENSORRT_DIR}/lib
                 CMAKE_FIND_ROOT_PATH_BOTH)
    add_launcher(NAME pytorch_tensorrt_benchmark
                 SOURCES ${SOURCES}
                 HEADERS ${HEADERS}
                 INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include" "${TORCH_TENSORRT_DIR}/include/"
                 DEPENDENCIES ${TORCH_LIBRARIES} ${TORCH_TENSORRT_LIB}
                 DEFINITIONS PYTORCH_TENSORRT)
endif()
