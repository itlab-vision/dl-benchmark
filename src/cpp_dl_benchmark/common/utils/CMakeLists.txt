set(TARGET_NAME "utils")

find_package(nlohmann_json REQUIRED HINTS /usr/lib/cmake)

file(GLOB_RECURSE HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/include/*")
file(GLOB_RECURSE SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/src/*")

add_library(${TARGET_NAME} STATIC ${HEADERS} ${SOURCES})
target_include_directories(${TARGET_NAME} PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}/include")
target_link_libraries(${TARGET_NAME} PRIVATE nlohmann_json::nlohmann_json)

check_code_style(NAME ${TARGET_NAME}
    CLANG_FORMAT ${ENABLE_CLANG_FORMAT})
