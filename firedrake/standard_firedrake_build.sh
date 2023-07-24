#!/bin/bash

curl -O https://raw.githubusercontent.com/firedrakeproject/firedrake/master/scripts/firedrake-install

source /data/home/jb1581/workspace/pileus/firedrake/standard_variables

echo PETSC_DIR is $PETSC_DIR

python3.11 firedrake-install \
    --no-package-manager \
    --honour-petsc-dir \
    --mpicc=$MPICC \
    --mpicxx=$MPICXX \
    --mpif90=$MPIF90 \
    --mpiexec=$MPIEXEC \
    --venv-name=firedrake-real-opt
