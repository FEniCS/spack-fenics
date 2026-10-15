# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

cmake_minimum_required(VERSION 3.19)
project(spack_smoke LANGUAGES CXX)
find_package(Basix REQUIRED CONFIG)
add_executable(smoke main.cpp)
target_compile_features(smoke PRIVATE cxx_std_20)
target_link_libraries(smoke PRIVATE Basix::basix)
