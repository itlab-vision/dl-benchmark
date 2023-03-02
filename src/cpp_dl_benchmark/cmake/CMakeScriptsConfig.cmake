# Copyright (C) 2023 KNS Group LLC (YADRO)
# All Rights Reserved.

# This software contains the intellectual property of YADRO
# or is licensed to YADRO from third parties. Use of this
# software and the intellectual property contained therein is expressly
# limited to the terms and conditions of the License Agreement under which
# it is provided by YADRO.
#

cmake_minimum_required(VERSION 3.10)

if(NOT DEFINED CMakeScripts_DIR)
    message(FATAL_ERROR "CMakeScripts_DIR is not defined")
endif()

set(CMAKE_MODULE_PATH "${CMakeScripts_DIR}")
set(OLD_CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH})

# Code style utils
include(clang_format/clang_format)

# Restore state
set(CMAKE_MODULE_PATH ${OLD_CMAKE_MODULE_PATH})