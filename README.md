# FEniCS Spack packages overlay repository

This Spack package repository contains Spack packages only for the FEniCS
Project components. Using `spack repo add` it can be overlaid onto any complete
upstream package repository. Its FEniCS component package will then take
precedence over the upstream package repository.

## Instructions

For full instructions on using `spack repo` see [the Spack
documentation](https://spack.readthedocs.io/en/latest/repositories.html).

TL;DR on a system with `spack` installed:

    spack repo add https://github.com/FEniCS/spack-fenics.git
    spack repo list

Alternatively, to work with this repository:

    spack repo list

You should see the `builtin` repository which points at a folder containing the
complete upstream Spack packages repository, e.g.:

    [+] builtin    v2.2    /Users/jack.hale/.spack/package_repos/fncqgg4/repos/spack_repo/builtin

Clone this repository:

    git clone https://github.com/FEniCS/spack-fenics.git

And add it as a repository:

    spack repo add spack-fenics/spack_repo/fenics

Run `spack repo list` again to show, e.g.:

    [+] fenics     v2.4    /Users/jack.hale/fenicsx-main/src/spack-fenics/spack_repo/fenics
    [+] builtin    v2.2    /Users/jack.hale/.spack/package_repos/fncqgg4/repos/spack_repo/builtin

Package definitions in `fenics` will now take precedence over duplicates in
`builtin`.

Running `spack spec -N fenics-dolfinx@0.9` should give, e.g.:

```
 -   fenics.fenics-dolfinx@0.9.0~adios2~ipo~petsc~slepc build_system=cmake build_type=RelWithDebInfo generator=make partitioners:=parmetis platform=darwin os=sequoia target=m1 %c,cxx=apple-clang@17.0.0
...
```

where `fenics.fenics-dolfinx` implies the use of the `fenics` repository.

## Maintenance commitment

We aim to keep the last three `x` versions `0.x.*` of `py-fenics-dolfinx`
building with PETSc, SLEPc, ADIOS2, Parmetis, SCOTCH and KaHIP support using
Ubuntu LTS-provided GCC and clang. Due to an unidentified performance issue we
are currently not running the test suite for `py-fenics-dolfinx@0.8`.

## Uses

1. Releasing Spack packages to users without waiting for PRs to be merged into
   the upstream `builtin` repository.
2. Allows experimentation with FEniCS Spack packages without having to maintain
   a full branch of the upstream `builtin` repository.

## Observations

### C++ ABIs

We have observed issues when two different compilers are selected by Spack to
build C++ components. This can lead to missing symbols at runtime error due to
different name mangling conventions and application binary interfaces (ABIs).
If this happens you can push the compiler down the Spack concretisation using
`%%`, e.g.:

    spack spec -N py-fenics-dolfinx %%clang@18

or a more precise approach using `^` and `%`, e.g.:

    spack spec -N py-fenics-dolfinx %clang@18 ^fenics-dolfinx %clang@18 ^py-fenics-basix %clang@18 ^fenics-basix %clang@18

### Reproducing complex build environment

To build C++ applications using Spack's build environment (e.g. when it used
special compilers to build fenics-dolfinx):

    spack load cmake fenics-dolfinx py-fenics-ffcx
    spack build-spec --dump spack-build-env.sh fenics-dolfinx
    source spack-build-env.sh
    # Execute e.g. cmake, should use Spack's compiler-wrapper 

## CI actions

A package job is a single call to the shared `test-package` action: it builds
a Spack environment, runs the package's tests, and pushes what it built to the
build cache. Nothing else belongs in the job. The cache push runs whatever the
outcome, so a failed or cancelled job still caches what it built, and it is
skipped for forked pull requests, which have no write access.

List the package under test first in the `spec` input. The Concretize step
checks the first concretized root against that first name and fails the job on
a mismatch, so a mis-ordered spec cannot quietly test the wrong package. Each
build uploads `log.xml`, `spack.yaml` and `spack.lock` for diagnosis and
reproduction, and a failing `spack test run` dumps its full log.

`test-mode` selects what happens to the root's own tests:

| Mode | Effect |
| --- | --- |
| `none` (default) | Plain installation; no tests, no test dependencies. |
| `dependencies` | Install the root's test dependencies so `spack test run` works, but leave the root free to come from the build cache. |
| `root` | Also build the root from source and run its install-time tests with `spack install --test=root`. |

In both testing modes the action then runs `spack test run` against the exact
installed root. Dependencies may still come from the build cache in either
mode; neither mode tests the dependencies themselves. Testing adds the root's
test dependencies to its hash, so a tested root is not the one other jobs
concretize. After the tests pass, the action also installs the root from a copy
of the environment concretized without tests, and pushes both to the cache.

Spack uses its clean build environment, which passes `MPIEXEC_PREFLAGS`
through untouched. The DOLFINx recipes parse it with shell quoting and forward
it to CMake's MPI tests and the Python suite's MPI launcher. When the root's
DAG contains Open MPI, the action sets it to `--allow-run-as-root
--oversubscribe`, since container jobs run as root; a value the caller sets
itself takes precedence, and MPICH jobs get no flags.

The package matrices run tests only through Spack. Suite selection, xdist
scheduling, compatibility exclusions and DOLFINx Python MPI runs belong to the
recipes; runners do not invoke pytest, CTest or MPI test commands directly.
DOLFINx and FFCx 0.8 use `test-mode: dependencies`, so they keep stand-alone
coverage while their full suites stay excluded.

The two kinds of recipe test have different scopes:

| Package | Install-time tests (`--test=root`) | Stand-alone tests (`spack test run`) |
| --- | --- | --- |
| C++ Basix | Upstream CMake installation check | Build and run the create-and-tabulate demo |
| C++ DOLFINx | C++ unit suite through CTest | Build and run the Poisson demo with PETSc, or interpolation/IO demo without PETSc |
| Python Basix | Upstream pytest suite | Run the create-and-tabulate demo |
| Python DOLFINx | Upstream Python unit suite | Run the matrix-free Poisson demo |
| Python FFCx | Upstream pytest suite | Compile the one-dimensional Poisson demo |
| Python UFL | Upstream pytest suite | Run the Poisson form example |

Both kinds of test build against the spec as installed. The C++ recipes reuse
Spack's standard CMake arguments, so a test configures the way the library
did: same `build_type`, same generator, and CMake's package registry stays
out of `find_package`, which would otherwise let a stale user build tree
answer in place of the installed package. Two of those defaults are replaced
— the standard `CMAKE_PREFIX_PATH` does not contain the install prefix the
tests link against, and the standard `CMAKE_INSTALL_PREFIX` points at the
package under test, which a throwaway build must never write into.

A spec's `cflags` and `cxxflags` reach the install-time checks but not the
stand-alone demos: Spack populates them from the build environment, which a
test context does not set up. The demos name the spec's compiler explicitly
and use it directly rather than through Spack's wrapper, which is what an
ordinary consumer of the installed CMake package would do.

Stand-alone tests reuse files from the matching upstream release. The recipes
save these files during installation with `cache_extra_test_sources`, so the
tests run against an installed package with no source or build directory left.
No custom smoke-test programs are maintained in this repository. Python
packages also inherit Spack's import checks.

## Developer notes

Diffing against an upstream `builtin` package set:

    export OTHER_PACKAGES_DIR=/path/to/spack-packages/repos/spack_repo/builtin/packages 
    cd spack-fenics/spack_repo/fenics/package
    for dir in */; do; git --no-pager diff --no-index $OTHER_PACKAGES_DIR/$dir $dir; done;
