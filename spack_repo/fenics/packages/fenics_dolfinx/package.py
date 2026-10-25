# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shlex

from spack_repo.builtin.build_systems.cmake import CMakeBuilder, CMakePackage

from spack.package import *


class FenicsDolfinx(CMakePackage):
    """Next generation FEniCS problem solving environment."""

    homepage = "https://github.com/FEniCS/dolfinx"
    git = "https://github.com/FEniCS/dolfinx.git"
    url = "https://github.com/FEniCS/dolfinx/archive/v0.1.0.tar.gz"
    maintainers("chrisrichardson", "garth-wells", "nate-sime", "jhale")
    license("LGPL-3.0-or-later")

    version("main", branch="main", no_cache=True)
    version(
        "0.11.0.post0", sha256="47c635cb82a99482d23e2e6bca26c31c9b2297bcad1ab5f5c651541caaaec68f"
    )
    version(
        "0.10.0.post4", sha256="3f827a88ab52843fbd7a5cc7814ecba165bdec65fd10df05eb031c286e8cd605"
    )
    version("0.9.0", sha256="b266c74360c2590c5745d74768c04568c965b44739becca4cd6b5aa58cdbbbd1")
    with default_args(deprecated=True):
        version("0.8.0", sha256="acf3104d9ecc0380677a6faf69eabfafc58d0cce43f7777e1307b95701c7cad9")

    patch("0.8-boost-filesystem.patch", when="@0.8")

    # CMake build types
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "Developer"),
    )

    # Graph partitioner variants
    variant(
        "partitioners",
        description="Graph partioning",
        default="parmetis",
        values=("kahip", "parmetis", "scotch"),
        multi=True,
    )

    depends_on("c", type="build")  # HDF5 dependency requires C in CMake config
    depends_on("cxx", type="build")

    conflicts("%gcc@:12", when="@0.10:")

    # Graph partitioner dependencies
    depends_on("kahip@3.12:", when="partitioners=kahip")
    depends_on("parmetis", when="partitioners=parmetis")
    depends_on("scotch+mpi", when="partitioners=scotch")
    # 0.9: finds SCOTCH in CMake CONFIG mode, which requires SCOTCH 7.0.1:
    depends_on("scotch@7.0.1:", when="@0.9: partitioners=scotch")

    variant("slepc", default=False, description="SLEPc support")
    variant("adios2", default=False, description="ADIOS2 support")
    variant("petsc", default=False, description="PETSc support")
    variant("superlu-dist", default=False, description="SuperLU_DIST support", when="@0.11:")

    conflicts("~petsc", when="+slepc", msg="+slepc requires +petsc")

    depends_on("cmake@3.26:", when="@0.11:", type=("build", "test"))
    depends_on("cmake@3.21:", when="@0.9:", type=("build", "test"))
    depends_on("cmake@3.19:", when="@:0.8", type=("build", "test"))
    # Build-only: Spack 1.2.2 fails to solve this virtual with both build and
    # test types. The build edge keeps it in the DAG, which is all the demo
    # test needs to name the executable.
    depends_on("pkgconfig", type="build")
    depends_on("mpi")
    # HDF5Interface.cpp #if H5_VERSION_GE are not precise enough.
    depends_on("hdf5+mpi@1.12:")
    depends_on("boost@1.81:", when="@main")
    depends_on("boost@1.70:")
    depends_on("boost@1.70:+timer", when="@:0.9")
    depends_on("pugixml")
    depends_on("spdlog", when="@0.9:")

    depends_on("petsc+mpi+shared", when="+petsc")
    with when("+slepc"):
        depends_on("petsc+mpi+shared")
        depends_on("slepc")

    depends_on("adios2@2.8.1:", when="@0.9: +adios2")
    depends_on("adios2@:2.10", when="@:0.9 +adios2")
    depends_on("adios2+mpi", when="+adios2")

    depends_on("superlu-dist", when="@0.11: +superlu-dist")

    for ver in ("main", "0.11", "0.10", "0.9", "0.8"):
        depends_on(f"fenics-ufcx@{ver}", when=f"@{ver}")
        depends_on(f"fenics-basix@{ver}", when=f"@{ver}")
        depends_on(f"py-fenics-ffcx@{ver}", when=f"@{ver}", type="test")
    depends_on("catch2@3:", type="test")

    depends_on("ninja", when="generator=ninja", type="test")
    depends_on("gmake", when="generator=make", type="test")

    root_cmakelists_dir = "cpp"

    # Unit tests are built against the installed library, not in the build
    # tree: cpp includes CTest, so BUILD_TESTING=ON would otherwise give the
    # default 'check' callback a target to run.
    build_time_test_callbacks = ()

    def cmake_args(self):
        return [
            self.define("DOLFINX_SKIP_BUILD_TESTS", True),
            self.define_from_variant("DOLFINX_ENABLE_PETSC", "petsc"),
            self.define_from_variant("DOLFINX_ENABLE_SLEPC", "slepc"),
            self.define_from_variant("DOLFINX_ENABLE_ADIOS2", "adios2"),
            self.define("DOLFINX_UFCX_PYTHON", False),
            self.define("DOLFINX_ENABLE_KAHIP", "partitioners=kahip" in self.spec),
            self.define("DOLFINX_ENABLE_PARMETIS", "partitioners=parmetis" in self.spec),
            self.define("DOLFINX_ENABLE_SCOTCH", "partitioners=scotch" in self.spec),
            self.define("DOLFINX_ENABLE_SUPERLU_DIST", "superlu-dist" in self.spec),
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
        # Set during a build only: Spack does not call
        # flags_to_build_system_args in a test context, so a spec's cflags
        # and cxxflags reach the install-time check but not the demo.
        args.extend(getattr(self, "cmake_flag_args", []))
        args.extend(self.define(name, value) for name, value in replaced.items())
        return args

    @staticmethod
    def _add_cxx_flag(args, flag):
        """Append a flag to either typed or untyped CMake compiler flags."""
        for i, arg in enumerate(args):
            if arg.startswith(("-DCMAKE_CXX_FLAGS=", "-DCMAKE_CXX_FLAGS:")):
                args[i] = f"{arg} {flag}"
                return args
        return args + [f"-DCMAKE_CXX_FLAGS={flag}"]

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Build and run the upstream C++ unit suite against installed DOLFINx."""
        test_dir = join_path(self.stage.path, "spack-test-build")
        args = self.installed_cmake_args(test_dir)
        # Forward caller-supplied launcher flags as a CMake list.
        args.append(
            self.define("MPIEXEC_PREFLAGS", shlex.split(os.environ.get("MPIEXEC_PREFLAGS", "")))
        )
        # Spack's llvm provider before Clang 19 lacks -Wno-c2y-extensions.
        if self.spec["cxx"].satisfies("llvm@:18"):
            args = self._add_cxx_flag(args, "-Wno-unknown-warning-option")
        cmake("-S", join_path(self.stage.source_path, "cpp", "test"), "-B", test_dir, *args)
        cmake("--build", test_dir, "--parallel", str(make_jobs))
        # Tests at different MPI sizes share output filenames.
        with working_dir(test_dir):
            ctest("--output-on-failure", "--parallel", "1")

    @property
    def demo_name(self):
        """Upstream demo exercised stand-alone; Poisson needs a PETSc solver."""
        return "poisson" if self.spec.satisfies("+petsc") else "interpolation-io"

    @run_after("install")
    def cache_test_sources(self):
        """Cache upstream demo sources for standalone Spack tests."""
        cache_extra_test_sources(self, join_path("cpp", "demo", self.demo_name))

    # do_test() skips the suite with a clear error when the spec has no
    # compiler, so the lookups below are safe.
    test_requires_compiler = True

    def test_demo(self):
        """Build and run an upstream demo against the installed library."""
        cmake = self.spec["cmake"].command
        demo = self.demo_name
        source = join_path(self.test_suite.current_test_cache_dir, "cpp", "demo", demo)
        build_dir = join_path(self.test_suite.test_dir_for_spec(self.spec), "demo-build")
        args = self.installed_cmake_args(build_dir)
        # Spack leaves CC and CXX unset in a test context, so name the
        # compilers instead of letting CMake find them on PATH. The demos
        # enable C as well as C++. The real compilers, not Spack's wrappers:
        # a demo is here to show that an ordinary consumer can build against
        # the installed CMake package.
        args.append(self.define("CMAKE_C_COMPILER", self.spec["c"].package.cc))
        args.append(self.define("CMAKE_CXX_COMPILER", self.spec["cxx"].package.cxx))
        # pkg-config is a build dependency, so it is not on PATH here.
        args.append(self.define("PKG_CONFIG_EXECUTABLE", self.spec["pkgconfig"].command.path))
        with test_part(self, "test_demo_build", purpose=f"build the {demo} demo"):
            cmake("-S", source, "-B", build_dir, *args)
            cmake("--build", build_dir, "--parallel", str(make_jobs))
        suffix = ".exe" if self.spec.satisfies("platform=windows") else ""
        executable = join_path(build_dir, "demo_" + demo + suffix)
        with test_part(self, "test_demo_run", purpose=f"run the {demo} demo"):
            Executable(executable)()
