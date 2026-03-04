cmake_minimum_required(VERSION 3.21)
project(nbody LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 CONFIG REQUIRED)

add_subdirectory(cpp)
