# Copyright (C) 2023 KNS Group LLC (YADRO)
# SPDX-License-Identifier: Apache-2.0
#

cmake_minimum_required(VERSION 3.13)
project(onnxruntime_benchmark)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

find_package(OpenCV REQUIRED core imgproc imgcodecs)
find_package(nlohmann_json REQUIRED HINTS /usr/lib/cmake)

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

add_subdirectory(thirdparty/gflags)

file(GLOB sources "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp" "${CMAKE_CURRENT_SOURCE_DIR}/main.cpp")
file(GLOB headers "${CMAKE_CURRENT_SOURCE_DIR}/include/*.h*")

add_executable(${PROJECT_NAME} ${sources} ${headers})

target_include_directories(${PROJECT_NAME} PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/include" ${ORT_INCLUDE})

target_link_libraries(${PROJECT_NAME} PRIVATE gflags nlohmann_json::nlohmann_json ${OpenCV_LIBRARIES} ${ORT_LIBRARIES})

set_target_properties(${PROJECT_NAME} PROPERTIES CXX_STANDARD 17 LINKER_LANGUAGE CXX)
