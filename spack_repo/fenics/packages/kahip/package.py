# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.kahip.package import Kahip as BuiltinKahip

from spack.package import *


class Kahip(BuiltinKahip):
    """KaHIP, built for the target in the spec rather than for the build host.

    Upstream's CMakeLists adds '-march=native' unless NONATIVEOPTIMIZATIONS is
    set, and does so via add_definitions(), so it lands after CMAKE_CXX_FLAGS
    and beats the '-march' Spack derives from the spec's target ('cxxflags='
    on the spec loses the same way). The resulting libkahip carries whatever
    the build host supported, which is fine locally and wrong in a buildcache:
    built on an AVX-512 machine it raises SIGILL on a consumer without it,
    which is what the 'partitioners=kahip' dolfinx tests hit.
    """

    def cmake_args(self):
        args = list(super().cmake_args())
        args.append(self.define("NONATIVEOPTIMIZATIONS", True))
        return args
