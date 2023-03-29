# search for ORT_INSTALL_DIR in env variables
if (NOT DEFINED ORT_INSTALL_DIR)
    if (DEFINED ENV{ORT_INSTALL_DIR})
        set(ORT_INSTALL_DIR $ENV{ORT_INSTALL_DIR})
    else()
        message(FATAL_ERROR "Could not find ONNX Runtime install directory")
    endif()
endif()

find_library(ORT_LIBRARIES onnxruntime
            ${ORT_INSTALL_DIR}/lib
            CMAKE_FIND_ROOT_PATH_BOTH)
find_path(ORT_INCLUDE onnxruntime_cxx_api.h
        ${ORT_INSTALL_DIR}/include/onnxruntime/core/session
        CMAKE_FIND_ROOT_PATH_BOTH)

file(GLOB_RECURSE HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/include/*")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*")

add_launcher(NAME onnxruntime_benchmark
    SOURCES ${SOURCES}
    HEADERS ${HEADERS}
    INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include" ${ORT_INCLUDE}
    DEPENDENCIES ${ORT_LIBRARIES}
    DEFINITIONS ORT_DEFAULT)
