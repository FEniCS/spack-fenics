# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess
import sys
from pathlib import Path

import basix.ufl
import ufl

coordinate = basix.ufl.element("Lagrange", "triangle", 1, shape=(2,))
mesh = ufl.Mesh(coordinate)
element = basix.ufl.element("Lagrange", "triangle", 1)
space = ufl.FunctionSpace(mesh, element)
u = ufl.TrialFunction(space)
v = ufl.TestFunction(space)
a = ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx

# Run the installed CLI on this file, exercising form loading and code generation.
if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "ffcx", __file__], check=True)
    for suffix in (".c", ".h"):
        output = Path("smoke" + suffix)
        assert output.is_file() and output.stat().st_size > 0
