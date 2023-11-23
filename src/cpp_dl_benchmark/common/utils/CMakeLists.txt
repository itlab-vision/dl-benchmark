set(TARGET_NAME "utils")

file(GLOB_RECURSE HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/include/*")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*")

add_library(${TARGET_NAME} STATIC ${HEADERS} ${SOURCES})
target_include_directories(${TARGET_NAME} PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_link_libraries(${TARGET_NAME} PRIVATE nlohmann_json::nlohmann_json)

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND CMAKE_CXX_COMPILER_VERSION VERSION_LESS 9)
    target_link_libraries(${TARGET_NAME} PRIVATE stdc++fs)
endif()

check_code_style(NAME ${TARGET_NAME}
    CLANG_FORMAT ${ENABLE_CLANG_FORMAT})
