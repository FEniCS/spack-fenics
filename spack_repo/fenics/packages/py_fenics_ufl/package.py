# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyFenicsUfl(PythonPackage):
    """The Unified Form Language (UFL) is a domain specific language for
    declaration of finite element discretizations of variational forms. More
    precisely, it defines a flexible interface for choosing finite element
    spaces and defining expressions for weak forms in a notation close to
    mathematical notation."""

    homepage = "https://fenicsproject.org/"
    url = "https://github.com/FEniCS/ufl/archive/2019.1.0.tar.gz"
    git = "https://github.com/FEniCS/ufl.git"
    maintainers("chrisrichardson", "garth-wells", "jhale")

    license("LGPL-3.0-or-later")

    version("main", branch="main", no_cache=True)
    version("2026.1.0", sha256="72c0e4ac3d2f648f30f860fd4e895d96415a77318cb4551c5dbc53dc644b7c96")
    version(
        "2025.2.0.post0", sha256="2182fed6d0fc41fd97244d73fe6aa95e50725e5ba8fe1b3b0f3f4d0215b45534"
    )
    version("2025.1.0", sha256="a3aedb6fd06bb43e954c96e7cccc190a29dc9a00287f95bc365dbfc81b43a5f9")
    version("2024.2.0", sha256="d9353d23ccbdd9887f8d6edab74c04fe06d818da972072081dbf0c25bc86f5a7")
    version(
        "2024.1.0.post1", sha256="6e38e93a2c8417271c9fb316e0d0ea5fe1101c6a37b2496fff8290e7ea7ead74"
    )
    with default_args(deprecated=True):
        version(
            "2023.2.0", sha256="d1d3209e8ebd4bd70513c26890f51823bac90edc956233c47bd8e686e064436e"
        )
        version(
            "2023.1.1.post0",
            sha256="9e6e87f1447635029cec42604f62a76bba84899beb4b8822af10389d1f93a9b6",
        )
        version(
            "2022.2.0", sha256="d6e18e06df5d7a626c3138d49a543914d68186afb6159c4d1a7cd72b2a199b02"
        )
        version(
            "2022.1.0", sha256="48359903d47fb397900d105fe4a60b459c50bbf9d9da78beb9accb54e4e4acaf"
        )
        version(
            "2021.1.0", sha256="130fdc09bb7fcd39dcd2618426912b8a25a03431d94575711068b38c666b4337"
        )
        version(
            "2019.1.0", sha256="46ac0df4e96327be10b9576d2b8fa8b2c4ca62d3c681d407f5718b162d3ca22d"
        )
        version(
            "2018.1.0", sha256="b0d4c2f43f396fd5609317b70d55b53b89c649962fc8a593f4e0e21607da211d"
        )
        version(
            "2017.2.0.post0",
            sha256="111e77707cd6731584b1041f405c2fd3f1752a86c51fd9c430524bd396f293b0",
        )
        version(
            "2017.2.0", sha256="0adff7a511185b20c38ddaccdeed6c1b2ecafe4b163c688bfd1316d5c3b1c00d"
        )
        version(
            "2017.1.0.post1",
            sha256="82c8170f44c2392c7e60aa86495df22cc209af50735af8115dc35aeda4b0ca96",
        )
        version("2016.2.0", tag="ufl-2016.2.0", commit="962d56f65821fb9c50ca4a5a858882c472243431")

    depends_on("python@3.11:", when="@2026.1.0:", type=("build", "run"))
    depends_on("python@3.10:", when="@2025.2.0:", type=("build", "run"))
    depends_on("python@3.9:", when="@2025.1.0:", type=("build", "run"))
    depends_on("python@3.8:", when="@2023.2.0:", type=("build", "run"))

    depends_on("py-setuptools@77:", when="@2025.1.0:", type="build")
    depends_on("py-setuptools@62:", when="@2023.2.0:", type="build")
    depends_on("py-setuptools@58:", when="@2022.1.0:2023.1.1.post0", type="build")
    depends_on("py-setuptools@40:", when="@2016.2.0:2021.1.0", type="build")
    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-pytest", type="test")
    depends_on("py-pytest-xdist", type="test")

    import_modules = ("ufl",)
    # Spack's install-time import check (test_imports) runs without the
    # install prefix on PYTHONPATH, so it cannot find the package.
    # check_install imports the installed package instead, and
    # test_imports still runs as a stand-alone test.
    install_time_test_callbacks = ()

    def installed_module_env(self):
        """Environment that makes the just-installed modules importable.

        Spack does not put the prefix on PYTHONPATH at build time, so install
        tests would import the staged sources instead. Reuse the run-time hook
        of python (or python-venv), which now has the installed files to find.
        """
        env = EnvironmentModifications()
        self.python_spec.package.setup_dependent_run_environment(env, self.spec)
        return env

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Run the upstream test suite against installed UFL."""
        python = self.spec["python"].command
        python.add_default_envmod(self.installed_module_env())
        args = ["-m", "pytest", "-v", "--import-mode=append", "-n", str(make_jobs), "."]
        # UFL 2025.2 fixes Python 3.14 borrowed-reference counts.
        if self.spec.satisfies("@:2025.1 ^python@3.14:"):
            args.extend(["-k", "not test_strip_form_arguments_strips_data_refs"])
        with working_dir(join_path(self.stage.source_path, "test")):
            python(*args)

    @property
    def poisson_demo(self):
        """Upstream demo: a .ufl form file until 2021.1, a script from 2022.1."""
        return join_path(
            "demo", "Poisson.py" if self.spec.satisfies("@2022.1:") else "Poisson.ufl"
        )

    @run_after("install")
    def cache_test_sources(self):
        """Cache upstream demo sources for standalone Spack tests."""
        sources = [self.poisson_demo]
        if self.spec.satisfies("@2025.2:"):
            sources.append(join_path("test", "utils.py"))
        cache_extra_test_sources(self, sources)

    def test_poisson(self):
        """Run the upstream Poisson form example."""
        cache = self.test_suite.current_test_cache_dir
        python = self.spec["python"].command
        if self.spec.satisfies("@2025.2:"):
            # Drop empty entries: a trailing separator would put the working
            # directory on sys.path.
            entries = [join_path(cache, "test"), os.environ.get("PYTHONPATH", "")]
            python.add_default_env("PYTHONPATH", os.pathsep.join(e for e in entries if e))
        demo = join_path(cache, self.poisson_demo)
        if self.spec.satisfies("@2022.1:"):
            python(demo)
        else:
            # Legacy .ufl forms rely on the namespace supplied by UFL's loader.
            python(
                "-c",
                "import sys; from ufl.algorithms.formfiles import load_ufl_file; "
                "load_ufl_file(sys.argv[1])",
                demo,
            )
