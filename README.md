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

## CI status

Latest CI result on `main` for each package, version and build variant. Click
a badge to see the workflow runs.

| Package | Variant | main | 0.11 | 0.10 | 0.9 | 0.8 |
| :-- | :-- | :-: | :-: | :-: | :-: | :-: |
| `fenics-basix` | GCC | [![fenics-basix (main, gcc)]][basix] | [![fenics-basix (0.11, gcc)]][basix] | [![fenics-basix (0.10, gcc)]][basix] | [![fenics-basix (0.9, gcc)]][basix] | [![fenics-basix (0.8, gcc)]][basix] |
|  | Clang | [![fenics-basix (main, clang)]][basix] | [![fenics-basix (0.11, clang)]][basix] | [![fenics-basix (0.10, clang)]][basix] | [![fenics-basix (0.9, clang)]][basix] | [![fenics-basix (0.8, clang)]][basix] |
| `py-fenics-basix` | GCC | [![py-fenics-basix (main, gcc)]][basix] | [![py-fenics-basix (0.11, gcc)]][basix] | [![py-fenics-basix (0.10, gcc)]][basix] | [![py-fenics-basix (0.9, gcc)]][basix] | [![py-fenics-basix (0.8, gcc)]][basix] |
|  | Clang | [![py-fenics-basix (main, clang)]][basix] | [![py-fenics-basix (0.11, clang)]][basix] | [![py-fenics-basix (0.10, clang)]][basix] | [![py-fenics-basix (0.9, clang)]][basix] | [![py-fenics-basix (0.8, clang)]][basix] |
| `fenics-ufcx` | GCC | [![fenics-ufcx (main)]][ffcx] | [![fenics-ufcx (0.11)]][ffcx] | [![fenics-ufcx (0.10)]][ffcx] | [![fenics-ufcx (0.9)]][ffcx] | [![fenics-ufcx (0.8)]][ffcx] |
| `py-fenics-ffcx` |  | [![py-fenics-ffcx (main)]][ffcx] | [![py-fenics-ffcx (0.11)]][ffcx] | [![py-fenics-ffcx (0.10)]][ffcx] | [![py-fenics-ffcx (0.9)]][ffcx] | [![py-fenics-ffcx (0.8)]][ffcx] |
| `fenics-dolfinx` | GCC | [![fenics-dolfinx (main, gcc)]][dolfinx] | [![fenics-dolfinx (0.11, gcc)]][dolfinx] | [![fenics-dolfinx (0.10, gcc)]][dolfinx] | [![fenics-dolfinx (0.9, gcc)]][dolfinx] | [![fenics-dolfinx (0.8, gcc)]][dolfinx] |
|  | Clang | [![fenics-dolfinx (main, clang)]][dolfinx] | [![fenics-dolfinx (0.11, clang)]][dolfinx] | [![fenics-dolfinx (0.10, clang)]][dolfinx] | [![fenics-dolfinx (0.9, clang)]][dolfinx] | [![fenics-dolfinx (0.8, clang)]][dolfinx] |
| `py-fenics-dolfinx` | Python 3.11, GCC | [![py-fenics-dolfinx (main, 3.11, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.11, 3.11, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.10, 3.11, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.9, 3.11, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.8, 3.11, gcc)]][dolfinx] |
|  | Python 3.11, Clang | [![py-fenics-dolfinx (main, 3.11, clang)]][dolfinx] | [![py-fenics-dolfinx (0.11, 3.11, clang)]][dolfinx] | [![py-fenics-dolfinx (0.10, 3.11, clang)]][dolfinx] | [![py-fenics-dolfinx (0.9, 3.11, clang)]][dolfinx] | [![py-fenics-dolfinx (0.8, 3.11, clang)]][dolfinx] |
|  | Python 3.14, GCC | [![py-fenics-dolfinx (main, 3.14, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.11, 3.14, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.10, 3.14, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.9, 3.14, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.8, 3.14, gcc)]][dolfinx] |
|  | Python 3.14, Clang | [![py-fenics-dolfinx (main, 3.14, clang)]][dolfinx] | [![py-fenics-dolfinx (0.11, 3.14, clang)]][dolfinx] | [![py-fenics-dolfinx (0.10, 3.14, clang)]][dolfinx] | [![py-fenics-dolfinx (0.9, 3.14, clang)]][dolfinx] | [![py-fenics-dolfinx (0.8, 3.14, clang)]][dolfinx] |
|  | Python 3.15, GCC | [![py-fenics-dolfinx (main, 3.15, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.11, 3.15, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.10, 3.15, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.9, 3.15, gcc)]][dolfinx] | [![py-fenics-dolfinx (0.8, 3.15, gcc)]][dolfinx] |
|  | Python 3.15, Clang | [![py-fenics-dolfinx (main, 3.15, clang)]][dolfinx] | [![py-fenics-dolfinx (0.11, 3.15, clang)]][dolfinx] | [![py-fenics-dolfinx (0.10, 3.15, clang)]][dolfinx] | [![py-fenics-dolfinx (0.9, 3.15, clang)]][dolfinx] | [![py-fenics-dolfinx (0.8, 3.15, clang)]][dolfinx] |
|  | Python 3.12, GCC, SuperLU_DIST |  | [![py-fenics-dolfinx (0.11, 3.12, gcc)]][dolfinx] |  |  |  |

The GCC builds of DOLFINx enable PETSc, SLEPc and ADIOS2; the Clang builds use
the default variants. See [the workflows](.github/workflows) for the exact
specs.

UFL has its own version numbers:

| Package | main | 2025.2 | 2025.1 | 2024.2 | 2024.1 |
| :-- | :-: | :-: | :-: | :-: | :-: |
| `py-fenics-ufl` | [![py-fenics-ufl (main)]][ufl] | [![py-fenics-ufl (2025.2)]][ufl] | [![py-fenics-ufl (2025.1)]][ufl] | [![py-fenics-ufl (2024.2)]][ufl] | [![py-fenics-ufl (2024.1)]][ufl] |

<!-- Badge labels are CI job names (see 'name:' in .github/workflows). -->
[basix]: https://github.com/FEniCS/spack-fenics/actions/workflows/basix.yml?query=branch%3Amain
[ffcx]: https://github.com/FEniCS/spack-fenics/actions/workflows/ffcx.yml?query=branch%3Amain
[ufl]: https://github.com/FEniCS/spack-fenics/actions/workflows/ufl.yml?query=branch%3Amain
[dolfinx]: https://github.com/FEniCS/spack-fenics/actions/workflows/dolfinx.yml?query=branch%3Amain
[fenics-basix (main, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(main,%20gcc)
[fenics-basix (0.11, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(0.11,%20gcc)
[fenics-basix (0.10, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(0.10,%20gcc)
[fenics-basix (0.9, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(0.9,%20gcc)
[fenics-basix (0.8, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(0.8,%20gcc)
[fenics-basix (main, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(main,%20clang)
[fenics-basix (0.11, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(0.11,%20clang)
[fenics-basix (0.10, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(0.10,%20clang)
[fenics-basix (0.9, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(0.9,%20clang)
[fenics-basix (0.8, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-basix%20(0.8,%20clang)
[py-fenics-basix (main, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(main,%20gcc)
[py-fenics-basix (0.11, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(0.11,%20gcc)
[py-fenics-basix (0.10, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(0.10,%20gcc)
[py-fenics-basix (0.9, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(0.9,%20gcc)
[py-fenics-basix (0.8, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(0.8,%20gcc)
[py-fenics-basix (main, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(main,%20clang)
[py-fenics-basix (0.11, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(0.11,%20clang)
[py-fenics-basix (0.10, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(0.10,%20clang)
[py-fenics-basix (0.9, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(0.9,%20clang)
[py-fenics-basix (0.8, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-basix%20(0.8,%20clang)
[fenics-ufcx (main)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-ufcx%20(main)
[fenics-ufcx (0.11)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-ufcx%20(0.11)
[fenics-ufcx (0.10)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-ufcx%20(0.10)
[fenics-ufcx (0.9)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-ufcx%20(0.9)
[fenics-ufcx (0.8)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-ufcx%20(0.8)
[py-fenics-ffcx (main)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ffcx%20(main)
[py-fenics-ffcx (0.11)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ffcx%20(0.11)
[py-fenics-ffcx (0.10)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ffcx%20(0.10)
[py-fenics-ffcx (0.9)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ffcx%20(0.9)
[py-fenics-ffcx (0.8)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ffcx%20(0.8)
[fenics-dolfinx (main, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(main,%20gcc)
[fenics-dolfinx (0.11, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(0.11,%20gcc)
[fenics-dolfinx (0.10, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(0.10,%20gcc)
[fenics-dolfinx (0.9, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(0.9,%20gcc)
[fenics-dolfinx (0.8, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(0.8,%20gcc)
[fenics-dolfinx (main, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(main,%20clang)
[fenics-dolfinx (0.11, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(0.11,%20clang)
[fenics-dolfinx (0.10, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(0.10,%20clang)
[fenics-dolfinx (0.9, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(0.9,%20clang)
[fenics-dolfinx (0.8, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=fenics-dolfinx%20(0.8,%20clang)
[py-fenics-dolfinx (main, 3.11, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(main,%203.11,%20gcc)
[py-fenics-dolfinx (0.11, 3.11, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.11,%203.11,%20gcc)
[py-fenics-dolfinx (0.10, 3.11, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.10,%203.11,%20gcc)
[py-fenics-dolfinx (0.9, 3.11, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.9,%203.11,%20gcc)
[py-fenics-dolfinx (0.8, 3.11, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.8,%203.11,%20gcc)
[py-fenics-dolfinx (main, 3.11, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(main,%203.11,%20clang)
[py-fenics-dolfinx (0.11, 3.11, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.11,%203.11,%20clang)
[py-fenics-dolfinx (0.10, 3.11, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.10,%203.11,%20clang)
[py-fenics-dolfinx (0.9, 3.11, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.9,%203.11,%20clang)
[py-fenics-dolfinx (0.8, 3.11, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.8,%203.11,%20clang)
[py-fenics-dolfinx (main, 3.14, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(main,%203.14,%20gcc)
[py-fenics-dolfinx (0.11, 3.14, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.11,%203.14,%20gcc)
[py-fenics-dolfinx (0.10, 3.14, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.10,%203.14,%20gcc)
[py-fenics-dolfinx (0.9, 3.14, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.9,%203.14,%20gcc)
[py-fenics-dolfinx (0.8, 3.14, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.8,%203.14,%20gcc)
[py-fenics-dolfinx (main, 3.14, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(main,%203.14,%20clang)
[py-fenics-dolfinx (0.11, 3.14, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.11,%203.14,%20clang)
[py-fenics-dolfinx (0.10, 3.14, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.10,%203.14,%20clang)
[py-fenics-dolfinx (0.9, 3.14, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.9,%203.14,%20clang)
[py-fenics-dolfinx (0.8, 3.14, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.8,%203.14,%20clang)
[py-fenics-dolfinx (main, 3.15, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(main,%203.15,%20gcc)
[py-fenics-dolfinx (0.11, 3.15, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.11,%203.15,%20gcc)
[py-fenics-dolfinx (0.10, 3.15, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.10,%203.15,%20gcc)
[py-fenics-dolfinx (0.9, 3.15, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.9,%203.15,%20gcc)
[py-fenics-dolfinx (0.8, 3.15, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.8,%203.15,%20gcc)
[py-fenics-dolfinx (main, 3.15, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(main,%203.15,%20clang)
[py-fenics-dolfinx (0.11, 3.15, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.11,%203.15,%20clang)
[py-fenics-dolfinx (0.10, 3.15, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.10,%203.15,%20clang)
[py-fenics-dolfinx (0.9, 3.15, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.9,%203.15,%20clang)
[py-fenics-dolfinx (0.8, 3.15, clang)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.8,%203.15,%20clang)
[py-fenics-dolfinx (0.11, 3.12, gcc)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-dolfinx%20(0.11,%203.12,%20gcc)
[py-fenics-ufl (main)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ufl%20(main)
[py-fenics-ufl (2025.2)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ufl%20(2025.2)
[py-fenics-ufl (2025.1)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ufl%20(2025.1)
[py-fenics-ufl (2024.2)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ufl%20(2024.2)
[py-fenics-ufl (2024.1)]: https://img.shields.io/github/check-runs/FEniCS/spack-fenics/main?label=&nameFilter=py-fenics-ufl%20(2024.1)

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

## Developer notes

Diffing against an upstream `builtin` package set:

    export OTHER_PACKAGES_DIR=/path/to/spack-packages/repos/spack_repo/builtin/packages 
    cd spack-fenics/spack_repo/fenics/package
    for dir in */; do; git --no-pager diff --no-index $OTHER_PACKAGES_DIR/$dir $dir; done;
