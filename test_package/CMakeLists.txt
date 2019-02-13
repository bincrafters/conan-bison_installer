project(test_package)
cmake_minimum_required(VERSION 2.8.11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(BISON REQUIRED)

BISON_TARGET(PARSER test_package.y ${CMAKE_CURRENT_BINARY_DIR}/test_package.cpp)
add_executable(${PROJECT_NAME} ${BISON_PARSER_OUTPUTS})
