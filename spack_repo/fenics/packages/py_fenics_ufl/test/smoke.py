# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import ufl
from ufl.algorithms import expand_derivatives

x = ufl.variable(ufl.as_ufl(3.0))
derivative = expand_derivatives(ufl.diff(x**2, x))
assert float(derivative) == 6.0
