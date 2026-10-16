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

    depends_on("ninja", when="generator=ninja", type="test")
    depends_on("gmake", when="generator=make", type="test")

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
    def check_install(self):
        test_dir = join_path(self.stage.path, "spack-test-build")
        generator = "Ninja" if self.spec.satisfies("generator=ninja") else "Unix Makefiles"
        args = CMakeBuilder.std_args(self, generator=generator)
        args.extend(getattr(self, "cmake_flag_args", []))
        args.append(self.define("CMAKE_PREFIX_PATH", [self.prefix, *get_cmake_prefix_path(self)]))
        cmake("-S", join_path(self.stage.source_path, "test", "test_cmake"), "-B", test_dir, *args)
        cmake("--build", test_dir, "--parallel", str(make_jobs))
        executable = "a.out.exe" if self.spec.satisfies("platform=windows") else "a.out"
        Executable(join_path(test_dir, executable))()

    @run_after("install")
    def cache_test_sources(self):
        sources = ["demo/cpp/demo_create_and_tabulate"]
        helper = "cmake/BasixPythonHints.cmake"
        if os.path.isfile(join_path(self.stage.source_path, helper)):
            sources.append(helper)
        cache_extra_test_sources(self, sources)

    test_requires_compiler = True

    def test_create_and_tabulate(self):
        """Build and run the upstream create-and-tabulate demo."""
        cmake = self.spec["cmake"].command
        source = join_path(
            self.test_suite.current_test_cache_dir, "demo", "cpp", "demo_create_and_tabulate"
        )
        generator = "Ninja" if self.spec.satisfies("generator=ninja") else "Unix Makefiles"
        args = CMakeBuilder.std_args(self, generator=generator)
        args.extend(getattr(self, "cmake_flag_args", []))
        args.append(self.define("CMAKE_PREFIX_PATH", [self.prefix, *get_cmake_prefix_path(self)]))
        # Spack 1.2.2 can omit compiler environment variables in test context.
        if not os.environ.get("CXX"):
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["cxx"].package.cxx))
        cmake("-S", source, "-B", "demo-build", *args)
        cmake("--build", "demo-build", "--parallel", str(make_jobs))
        suffix = ".exe" if self.spec.satisfies("platform=windows") else ""
        executable = join_path("demo-build", "demo_create_and_tabulate" + suffix)
        Executable(executable)()
