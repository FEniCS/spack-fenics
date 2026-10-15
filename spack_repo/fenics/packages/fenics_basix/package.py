# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.cmake import CMakeBuilder, CMakePackage

from spack.package import *


class FenicsBasix(CMakePackage):
    """Basix is a finite element definition and tabulation runtime library"""

    homepage = "https://github.com/FEniCS/basix"
    url = "https://github.com/FEniCS/basix/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/basix.git"
    maintainers("mscroggs", "chrisrichardson", "garth-wells", "jhale")

    license("MIT")

    version("main", branch="main", no_cache=True)
    version("0.11.0", sha256="bb4355f4cd3c98d5e944c2b8596f3240225d0a8ab3bd1344133d2056a7b2c388")
    version(
        "0.10.0.post0", sha256="11a6482fb8d7204fbd77aaf457a9ae3e75db1707b3e30ea2c938eccfee925ea4"
    )
    version("0.10.0", sha256="b93221dac7d3fea8c10e77617f6201036de35d0c5437440b718de69a28c3773f")
    version("0.9.0", sha256="60e96b2393084729b261cb10370f0e44d12735ab3dbd1f15890dec23b9e85329")
    with default_args(deprecated=True):
        version("0.8.0", sha256="b299af82daf8fa3e4845e17f202491fe71b313bf6ab64c767a5287190b3dd7fe")

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "Developer"),
    )

    depends_on("cxx", type="build")
    # test/test_cmake enables C as well as C++.
    depends_on("c", type="build")

    depends_on("cmake@3.21:", when="@0.9:", type=("build", "test"))
    depends_on("cmake@3.19:", when="@:0.8", type=("build", "test"))
    depends_on("blas")
    depends_on("lapack")

    conflicts("%gcc@:9.10", msg="fenics-basix requires GCC-10 or newer for C++20 support")
    conflicts("%clang@:9.10", msg="fenics-basix requires Clang-10 or newer for C++20 support")

    depends_on("ninja", type="test")

    root_cmakelists_dir = "cpp"
    build_time_test_callbacks = ()

    # Required for compatibility of Cray HPE systems
    def cmake_args(self):
        return [
            "-DBLAS_LIBRARIES=" + self.spec["blas"].libs.joined(";"),
            "-DLAPACK_LIBRARIES=" + self.spec["lapack"].libs.joined(";"),
        ]

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        test_dir = join_path(self.stage.path, "spack-test-build")
        generator = "Ninja" if self.spec.satisfies("generator=ninja") else "Unix Makefiles"
        args = CMakeBuilder.std_args(self, generator=generator)
        args.extend(getattr(self, "cmake_flag_args", []))
        # GNUInstallDirs puts CMAKE_INSTALL_LIBDIR at lib64 on some distributions.
        libdir = next(
            (
                d
                for d in (self.prefix.lib, self.prefix.lib64)
                if os.path.isdir(join_path(d, "cmake", "basix"))
            ),
            self.prefix.lib,
        )
        args.extend(
            [
                self.define("CMAKE_BUILD_TYPE", "Developer"),
                self.define("Basix_DIR", join_path(libdir, "cmake", "basix")),
            ]
        )
        cmake("-S", join_path(self.stage.source_path, "test", "test_cmake"), "-B", test_dir, *args)
        cmake("--build", test_dir, "--parallel", str(make_jobs))
        executable = "a.out.exe" if self.spec.satisfies("platform=windows") else "a.out"
        Executable(join_path(test_dir, executable))()

    test_requires_compiler = True

    def test_link(self):
        """Compile and run a small client against the installed library."""
        cmake = self.spec["cmake"].command
        source = self.test_suite.current_test_data_dir
        prefixes = ";".join(str(dep.prefix) for dep in self.spec.traverse(deptype=("link", "run")))
        cmake(
            "-S",
            source,
            "-B",
            "smoke-build",
            "-G",
            "Ninja",
            "-DCMAKE_BUILD_TYPE=Developer",
            f"-DCMAKE_CXX_COMPILER={self.spec['cxx'].package.cxx}",
            f"-DCMAKE_PREFIX_PATH={prefixes}",
        )
        cmake("--build", "smoke-build")
        suffix = ".exe" if self.spec.satisfies("platform=windows") else ""
        executable = join_path("smoke-build", "smoke" + suffix)
        Executable(executable)()
