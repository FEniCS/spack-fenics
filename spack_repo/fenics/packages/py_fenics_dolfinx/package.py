# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyFenicsDolfinx(PythonPackage):
    """Python interface to the next generation FEniCS problem solving
    environment."""

    homepage = "https://github.com/FEniCS/dolfinx"
    url = "https://github.com/FEniCS/dolfinx/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/dolfinx.git"
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

    # Backport the test condition from DOLFINx aa9570ddf8 (#4397).
    patch("cffi-complex-skip.patch", when="@0.10:0.11")

    # CMake build type
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "Developer"),
    )

    variant("petsc4py", default=False, description="petsc4py support")
    variant("slepc4py", default=False, description="slepc4py support")

    # py-fenics-dolfinx does not require a C compiler, but does depend
    # on DOLFINXConfig.cmake which in turn includes hdf5-config.cmake.
    # When HDF5 has MPI support, hdf5-config.cmake calls
    # enable_language(c).
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.26:", when="@0.11:", type="build")
    depends_on("cmake@3.21:", when="@0.9:", type="build")
    depends_on("cmake@3.19:", when="@:0.8", type="build")
    depends_on("hdf5", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("python@3.11:", when="@0.11:", type=("build", "run"))
    depends_on("python@3.10:", when="@0.10:", type=("build", "run"))
    depends_on("python@3.9:", when="@0.8:", type=("build", "run"))
    depends_on("python@3.8:3.10", when="@0.6", type=("build", "run"))

    for ver in ["main", "0.11.0.post0", "0.10.0.post4", "0.9.0", "0.8.0"]:
        depends_on(f"fenics-dolfinx@{ver}", when=f"@{ver}")

    for ver in ["main", "0.11", "0.10", "0.9", "0.8"]:
        depends_on(f"fenics-basix@{ver}", type=("build", "link"), when=f"@{ver}")
        depends_on(f"py-fenics-basix@{ver} +ufl", type=("build", "run"), when=f"@{ver}")
        depends_on(f"py-fenics-ffcx@{ver}", type=("build", "run"), when=f"@{ver}")

    for ufl_ver, ver in [
        ("main", "main"),
        ("2026.1", "0.11"),
        ("2025.2", "0.10"),
        ("2024.2", "0.9"),
        ("2024.1", "0.8"),
    ]:
        depends_on(f"py-fenics-ufl@{ufl_ver}", type=("build", "run"), when=f"@{ver}")

    depends_on("py-numpy@2:", when="@0.11:", type=("build", "run"))
    depends_on("py-numpy@1.21:", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))

    conflicts("~petsc4py", when="+slepc4py", msg="+slepc4py requires +petsc4py")
    # petsc4py only an optional dependency 0.9 and later.
    with when("@:0.8"):
        depends_on("fenics-dolfinx +petsc")
        depends_on("py-petsc4py", type=("build", "run"))
    with when("+petsc4py"):
        depends_on("fenics-dolfinx +petsc")
        depends_on("py-petsc4py", type=("build", "run"))
    with when("+slepc4py"):
        depends_on("fenics-dolfinx +petsc +slepc")
        depends_on("py-petsc4py", type=("build", "run"))
        depends_on("py-slepc4py", type=("build", "run"))

    depends_on("py-cffi", type=("build", "run"))

    depends_on("py-nanobind@2.9.2:", when="@0.11:", type="build")
    depends_on("py-nanobind@2.5:", when="@0.10:", type="build")
    # 2.2, not 2: 2.0.0 and 2.1.0 build, then fail all 119 interpolation
    # tests with "incompatible function arguments". 2.2.0 is the oldest
    # that passes (there is no 2.3.0).
    depends_on("py-nanobind@2.2:", when="@0.9:", type="build")
    depends_on("py-nanobind@1.8:1.9", when="@0.8", type="build")
    # nanobind 2.14 tightened argument conversion, so every form built by
    # 0.9-0.11 raises the same "incompatible function arguments" error.
    # They are clean on 2.13.0. Released versions only: main is adapted
    # and passes on 2.15.0.
    depends_on("py-nanobind@:2.13", when="@0.9:0.11", type="build")
    # +pyproject removed in py-scikit-build-core version 1
    depends_on("py-scikit-build-core@1:", when="@main", type="build")
    depends_on("py-scikit-build-core@0.11: +pyproject", when="@0.11:", type="build")
    depends_on("py-scikit-build-core@0.10: +pyproject", when="@0.9:", type="build")
    depends_on("py-scikit-build-core@0.5: +pyproject", when="@0.8:0.9", type="build")

    depends_on("py-pytest@9:", when="@0.10:", type="test")
    # Older releases define both pytest TOML tables, which pytest 9 rejects.
    depends_on("py-pytest@:8", when="@:0.9", type="test")
    depends_on("py-pytest-xdist", type="test")
    depends_on("py-scipy", type="test")
    depends_on("py-matplotlib", type="test")
    depends_on("py-networkx", when="@0.10:", type="test")
    depends_on("py-packaging", when="@0.10:", type="test")
    depends_on("py-sympy", when="@:0.8", type="test")
    depends_on("adios2+python", when="^fenics-dolfinx+adios2", type="test")

    def config_settings(self, spec, prefix):
        return {
            "build.tool-args": f"-j{make_jobs}",
            "build.verbose": "true",
            "cmake.build-type": spec.variants["build_type"].value,
        }

    build_directory = "python"

    import_modules = ("dolfinx",)

    def setup_build_environment(self, env):
        # Spack clears *_ROOT variables; preserve explicit MPI container opt-ins.
        for name in ("OMPI_ALLOW_RUN_AS_ROOT", "PRTE_ALLOW_RUN_AS_ROOT"):
            if name in os.environ:
                env.set(name, os.environ[name])
        python_pkg = self.spec["python"].package
        for directory in {python_pkg.platlib, python_pkg.purelib}:
            env.prepend_path("PYTHONPATH", join_path(self.prefix, directory))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        args = ["-m", "pytest", "-v", "--import-mode=importlib", "python/test/unit"]
        markers = []
        if self.spec.satisfies("@0.9: ~petsc4py"):
            markers.append("not petsc4py")
        if self.spec.satisfies("@0.9: ^fenics-dolfinx~adios2"):
            markers.append("not adios2")
        if markers:
            args.extend(["-m", " and ".join(markers)])

        # Retain known upstream release/compiler exclusions for both MPI sizes.
        excluded = ["test_cffi_expression"]
        if self.spec.satisfies("@0.9"):
            excluded.append("test_cube_distance")
            if self.spec["cxx"].satisfies("clang@18"):
                excluded.append("test_refine_interval")
        if self.spec.satisfies("@0.10:"):
            excluded.append("test_symmetry_interior_facet_assembly[mesh1]")
        # Python 3.14 changed reference-count semantics.
        if self.spec.satisfies("@0.9:0.10 ^python@3.14:"):
            excluded.append("test_mpi_comm_refcount")
        # Exact PETSc matrix equality is sensitive to the BLAS implementation.
        if self.spec.satisfies("@0.9:0.11 ^netlib-lapack"):
            excluded.append("test_matrix_assembly_rectangular")
        args.extend(["-k", " and ".join("not " + name for name in excluded)])

        python = self.spec["python"].command
        mpiexec = Executable(join_path(self.spec["mpi"].prefix.bin, "mpiexec"))
        with working_dir(self.stage.source_path):
            python(*args, "-n", str(make_jobs))
            mpiexec("-n", "3", python.path, *args)

    @property
    def poisson_demo(self):
        name = (
            "demo_poisson-matrix-free.py"
            if self.spec.satisfies("@0.11:")
            else "demo_poisson_matrix_free.py"
        )
        return join_path("python", "demo", name)

    @run_after("install")
    def cache_test_sources(self):
        cache_extra_test_sources(self, self.poisson_demo)

    def test_poisson(self):
        """Run the upstream matrix-free Poisson demo, including PETSc-free builds."""
        self.spec["python"].command(
            join_path(self.test_suite.current_test_cache_dir, self.poisson_demo)
        )
