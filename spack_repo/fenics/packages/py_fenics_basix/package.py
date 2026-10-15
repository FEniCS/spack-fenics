# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyFenicsBasix(PythonPackage):
    """Python interface to Basix, a finite element definition and tabulation runtime library"""

    homepage = "https://github.com/FEniCS/basix"
    url = "https://github.com/FEniCS/basix/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/basix.git"
    maintainers("chrisrichardson", "mscroggs", "garth-wells", "jhale")

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

    # Basix 0.8 wraps nanobind enums; extract their integer value directly.
    patch("enum-int.patch", when="@0.8")

    # CMake build type
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "Developer"),
    )

    variant("ufl", default=False, description="UFL support")

    depends_on("cxx", type="build")

    for ver in ("main", "0.11.0", "0.10.0.post0", "0.10.0", "0.9.0", "0.8.0"):
        depends_on(f"fenics-basix@{ver}", type=("build", "run"), when=f"@{ver}")

    # See python/CMakeLists.txt
    depends_on("cmake@3.21:", when="@0.9:", type="build")
    depends_on("cmake@3.19:", when="@0.8", type="build")
    depends_on("cmake@3.16:", when="@:0.7", type="build")

    # See python/pyproject.toml
    depends_on("python@3.11:", when="@0.11:", type=("build", "run"))
    depends_on("python@3.10:", when="@0.10:", type=("build", "run"))
    depends_on("python@3.9:", when="@0.8:", type=("build", "run"))
    depends_on("python@3.8:", when="@:0.7", type=("build", "run"))
    depends_on("py-numpy@2:", when="@:0.11", type=("build", "run"))
    depends_on("py-numpy@1.21:", type=("build", "run"))
    depends_on("py-pybind11@2.9.1:", when="@:0.7", type="build")
    depends_on("py-setuptools@42:", when="@:0.7", type="build")
    depends_on("py-nanobind@2.5:", when="@0.10:", type="build")
    depends_on("py-nanobind@2:", when="@0.9:", type="build")
    depends_on("py-nanobind@1.6.0:", when="@0.8:0.9", type="build")
    depends_on("py-scikit-build-core+pyproject@0.11:", when="@0.11:", type="build")
    depends_on("py-scikit-build-core+pyproject@0.10:", when="@0.10:", type="build")
    depends_on("py-scikit-build-core+pyproject@0.5.0:", when="@0.8:0.9", type="build")

    for ufl_ver, ver in [
        ("main", "main"),
        ("2026.1", "0.11"),
        ("2025.2", "0.10"),
        ("2024.2", "0.9"),
        ("2024.1", "0.8"),
    ]:
        depends_on(f"py-fenics-ufl@{ufl_ver}", type="run", when=f"@{ver} +ufl")
        depends_on(f"py-fenics-ufl@{ufl_ver}", type="test", when=f"@{ver}")
    depends_on("py-pytest", type="test")
    depends_on("py-pytest-xdist", type="test")
    depends_on("py-sympy", type="test")
    depends_on("py-scipy", type="test")
    depends_on("py-matplotlib", type="test")

    def config_settings(self, spec, prefix):
        return {
            "build.tool-args": f"-j{make_jobs}",
            "build.verbose": "true",
            "cmake.build-type": spec.variants["build_type"].value,
        }

    build_directory = "python"

    import_modules = ("basix",)

    def setup_build_environment(self, env):
        python_pkg = self.spec["python"].package
        for directory in {python_pkg.platlib, python_pkg.purelib}:
            env.prepend_path("PYTHONPATH", join_path(self.prefix, directory))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        python = self.spec["python"].command
        args = ["-m", "pytest", "-v", "--import-mode=importlib", "-n", str(make_jobs), "test"]
        if self.spec.satisfies("@0.8"):
            args.extend(["-k", "not test_all_elements_included"])
        with working_dir(self.stage.source_path):
            python(*args)

    @run_after("install")
    def cache_test_sources(self):
        cache_extra_test_sources(self, "demo/python/demo_create_and_tabulate.py")

    def test_create_and_tabulate(self):
        """Run the upstream create-and-tabulate demo."""
        demo = join_path(
            self.test_suite.current_test_cache_dir, "demo", "python", "demo_create_and_tabulate.py"
        )
        self.spec["python"].command(demo)
