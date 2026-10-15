# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

cmake_minimum_required(VERSION 3.19)
project(spack_smoke LANGUAGES C CXX)
find_package(DOLFINX REQUIRED CONFIG)
add_executable(smoke main.cpp)
target_compile_features(smoke PRIVATE cxx_std_20)
if(TARGET dolfinx::dolfinx)
  target_link_libraries(smoke PRIVATE dolfinx::dolfinx)
else()
  target_link_libraries(smoke PRIVATE dolfinx)
endif()
