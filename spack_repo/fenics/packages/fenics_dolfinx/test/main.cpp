// Copyright Spack Project Developers. See COPYRIGHT file for details.
//
// SPDX-License-Identifier: (Apache-2.0 OR MIT)

#include <dolfinx/common/IndexMap.h>
#include <mpi.h>

int main(int argc, char *argv[]) {
  MPI_Init(&argc, &argv);
  int result = 0;
  {
    dolfinx::common::IndexMap map(MPI_COMM_WORLD, 4);
    int ranks = 0;
    MPI_Comm_size(MPI_COMM_WORLD, &ranks);
    result = map.size_local() == 4 && map.size_global() == 4 * ranks ? 0 : 1;
  }
  MPI_Finalize();
  return result;
}
