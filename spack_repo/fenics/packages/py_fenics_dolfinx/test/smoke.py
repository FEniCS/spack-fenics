# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import numpy as np
from dolfinx import fem, mesh
from mpi4py import MPI

msh = mesh.create_unit_interval(MPI.COMM_WORLD, 4)
space = fem.functionspace(msh, ("Lagrange", 1))
f = fem.Function(space)
f.interpolate(lambda x: 1 + 2 * x[0])
assert msh.topology.index_map(1).size_global == 4
assert np.allclose(f.x.array, 1 + 2 * space.tabulate_dof_coordinates()[:, 0])
