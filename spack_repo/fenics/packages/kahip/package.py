# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.kahip.package import Kahip as BuiltinKahip

from spack.package import *


class Kahip(BuiltinKahip):
    """KaHIP, built for the target in the spec rather than for the build host.

    Upstream's CMakeLists adds '-march=native' unless NONATIVEOPTIMIZATIONS is
    set, and it adds it with add_definitions(), so it lands after
    CMAKE_CXX_FLAGS and beats the '-march' Spack derives from the spec's
    target. A 'cxxflags=' on the spec loses to it for the same reason. The
    result is a libkahip carrying whatever instructions the build host
    happened to support, which is fine for a local install and wrong for
    anything published to a buildcache: a kahip built on an AVX-512 machine
    raises SIGILL on a consumer without it. That is what the
    'partitioners=kahip' dolfinx tests hit when they take kahip from the
    cache.

    Setting the option makes the spec's target the thing actually compiled
    for, so the binary is usable on any host meeting it.
    """

    def cmake_args(self):
        args = list(super().cmake_args())
        args.append(self.define("NONATIVEOPTIMIZATIONS", True))
        return args
