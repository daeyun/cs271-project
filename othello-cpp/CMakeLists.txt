cmake_minimum_required(VERSION 3.7)
project(othello_cpp)

set(CMAKE_CXX_STANDARD 14)

add_definitions(-DGSL_THROW_ON_CONTRACT_VIOLATION)

find_package(OpenMP REQUIRED)

#set(CMAKE_C_COMPILER "gcc-7")
#set(CMAKE_CXX_COMPILER "g++-7")

set(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
set(CMAKE_VERBOSE_MAKEFILE ON)
SET(BUILD_SHARED_LIBS OFF)
#set(CMAKE_SHARED_LINKER_FLAGS  "-static-libgcc -static-libstdc++ -static")
#set(CMAKE_SHARED_LINKER_FLAGS  " -static")
set(CMAKE_SHARED_LINKER_FLAGS  " -static-libgcc -static-libstdc++")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 ${OpenMP_CXX_FLAGS}")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -O3 ${OpenMP_C_FLAGS}")

add_library(othello SHARED othello_ctypes.cc othello.h)
set_property(TARGET othello PROPERTY POSITION_INDEPENDENT_CODE ON)

add_executable(othello_test othello_test.cc othello.h)
