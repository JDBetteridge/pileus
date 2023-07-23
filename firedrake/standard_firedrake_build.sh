#!/bin/bash

curl -O https://raw.githubusercontent.com/firedrakeproject/firedrake/master/scripts/firedrake-install

export DEPENDENCIES_BASE_DIR=/data/shared/jb1581
export PACKAGES=$DEPENDENCIES_BASE_DIR/petsc/packages
export MPICH_DIR=$PACKAGES/bin
export PETSC_DIR=$DEPENDENCIES_BASE_DIR/petsc
export PETSC_ARCH=real-opt
export HDF5_DIR=$PACKAGES

source $DEPENDENCIES_BASE_DIR/spack/share/spack/setup-env.sh
spack load flex
spack load gcc@13.1
spack load python@3.11

python3 firedrake-install \
    --no-package-manager \
    --honour-petsc-dir \
    --mpicc=$MPICH_DIR/mpicc \
    --mpicxx=$MPICH_DIR/mpicxx \
    --mpif90=$MPICH_DIR/mpif90 \
    --mpiexec=$MPICH_DIR/mpiexec \
    --venv-name=firedrake_py311_real_opt
