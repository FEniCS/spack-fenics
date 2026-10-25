# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    patch("installation-check-cxx20.patch", when="@0.9:0.11")

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "Developer"),
    )

    depends_on("cxx", type="build")
    # test/test_cmake names no languages, so it enables C as well as C++.
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

    # Required for compatibility of Cray HPE systems
    def cmake_args(self):
        return [
            "-DBLAS_LIBRARIES=" + self.spec["blas"].libs.joined(";"),
            "-DLAPACK_LIBRARIES=" + self.spec["lapack"].libs.joined(";"),
        ]

    def installed_cmake_args(self, build_dir):
        """Preserve build settings when compiling against the installed library.

        Two of std_args' defaults are replaced: its CMAKE_PREFIX_PATH lacks
        the prefix the tests link against, and its CMAKE_INSTALL_PREFIX aims
        at the package under test, which a throwaway build must never write
        into.
        """
        generator = "Ninja" if self.spec.satisfies("generator=ninja") else "Unix Makefiles"
        replaced = {
            "CMAKE_PREFIX_PATH": [self.prefix, *get_cmake_prefix_path(self)],
            "CMAKE_INSTALL_PREFIX": join_path(build_dir, "install"),
        }
        args = [
            arg
            for arg in CMakeBuilder.std_args(self, generator=generator)
            if not arg.startswith(tuple(f"-D{name}:" for name in replaced))
        ]
        args.extend(getattr(self, "cmake_flag_args", []))
        args.extend(self.define(name, value) for name, value in replaced.items())
        return args

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Build and run the upstream CMake check against installed Basix."""
        test_dir = join_path(self.stage.path, "spack-test-build")
        args = self.installed_cmake_args(test_dir)
        cmake("-S", join_path(self.stage.source_path, "test", "test_cmake"), "-B", test_dir, *args)
        cmake("--build", test_dir, "--parallel", str(make_jobs))
        executable = "a.out.exe" if self.spec.satisfies("platform=windows") else "a.out"
        Executable(join_path(test_dir, executable))()

    @run_after("install")
    def cache_test_sources(self):
        """Cache upstream demo sources for standalone Spack tests."""
        sources = [join_path("demo", "cpp", "demo_create_and_tabulate")]
        # The demo picks up the Python hints module from @main onwards.
        if self.spec.satisfies("@main"):
            sources.append(join_path("cmake", "BasixPythonHints.cmake"))
        cache_extra_test_sources(self, sources)

    # do_test() skips the suite with a clear error when the spec has no
    # compiler, so the lookups below are safe.
    test_requires_compiler = True

    def test_create_and_tabulate(self):
        """Build and run the upstream create-and-tabulate demo."""
        cmake = self.spec["cmake"].command
        source = join_path(
            self.test_suite.current_test_cache_dir, "demo", "cpp", "demo_create_and_tabulate"
        )
        build_dir = join_path(self.test_suite.test_dir_for_spec(self.spec), "demo-build")
        # Test contexts do not initialize cmake_flag_args. Pass the spec's
        # flags explicitly so ABI settings also reach the consumer build.
        flags = {
            name: self.spec.compiler_flags.get(name, [])
            for name in self.spec.compiler_flags.valid_compiler_flags()
        }
        self.flags_to_build_system_args(flags)
        args = self.installed_cmake_args(build_dir)
        # Spack leaves CXX unset in test contexts; select the spec's compiler.
        args.append(self.define("CMAKE_CXX_COMPILER", self.spec["cxx"].package.cxx))
        with test_part(self, "test_create_and_tabulate_build", purpose="build the demo"):
            cmake("-S", source, "-B", build_dir, *args)
            cmake("--build", build_dir, "--parallel", str(make_jobs))
        suffix = ".exe" if self.spec.satisfies("platform=windows") else ""
        executable = join_path(build_dir, "demo_create_and_tabulate" + suffix)
        with test_part(self, "test_create_and_tabulate_run", purpose="run the demo"):
            Executable(executable)()
