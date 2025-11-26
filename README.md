# FEniCS Spack packages overlay repository

This Spack package repository contains Spack packages only for the FEniCS
Project components. Using `spack repo add` it can be overlaid onto any complete
upstream package repository. Its FEniCS component package will then take
precedence over the upstream package repository.

## Instructions

For full instructions on using `spack repo` see [the Spack
documentation](https://spack.readthedocs.io/en/latest/repositories.html).

On a system with Spack setup:

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

Running `spack spec -N fenics-dolfinx` should give output like:

```
 -   fenics.fenics-dolfinx@0.9.0~adios2~ipo~petsc~slepc build_system=cmake build_type=RelWithDebInfo generator=make partitioners:=parmetis platform=darwin os=sequoia target=m1 %c,cxx=apple-clang@17.0.0
[e]      ^builtin.apple-clang@17.0.0 build_system=bundle platform=darwin os=sequoia target=aarch64
```

where `fenics.fenics-dolfinx` implies the use of the `fenics` repository.

## Uses

1. Releasing Spack packages to users without waiting for PRs to be merged into
   the upstream `builtin` repository.
2. Allows experimentation with FEniCS Spack packages without having to maintain
   a full branch of the upstream `builtin` repository. 
