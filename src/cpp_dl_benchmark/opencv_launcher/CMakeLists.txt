# Copyright (C) 2023 KNS Group LLC (YADRO)
# SPDX-License-Identifier: Apache-2.0
#

find_package(OpenCV REQUIRED dnn)

file(GLOB_RECURSE HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/include/*")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*")

add_launcher(NAME opencv_dnn_benchmark
    SOURCES ${SOURCES}
    HEADERS ${HEADERS}
    INCLUDE_DIRECTORIES "${CMAKE_CURRENT_SOURCE_DIR}/include"
    DEPENDENCIES opencv_dnn
    DEFINITIONS OCV_DNN)
