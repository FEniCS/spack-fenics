# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import basix
import numpy as np

points = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
element = basix.create_element(
    basix.ElementFamily.P, basix.CellType.triangle, 1, basix.LagrangeVariant.equispaced
)
values = element.tabulate(0, points)[0, :, :, 0]
assert element.dim == 3
assert np.allclose(values, np.eye(3))
