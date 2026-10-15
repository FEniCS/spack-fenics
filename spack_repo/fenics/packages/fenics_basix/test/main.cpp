// Copyright Spack Project Developers. See COPYRIGHT file for details.
//
// SPDX-License-Identifier: (Apache-2.0 OR MIT)

#include <basix/finite-element.h>

int main() {
  auto element = basix::create_element<double>(
      basix::element::family::P, basix::cell::type::triangle, 1,
      basix::element::lagrange_variant::equispaced,
      basix::element::dpc_variant::unset, false);
  return element.dim() == 3 ? 0 : 1;
}
