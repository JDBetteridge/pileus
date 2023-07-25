#!/bin/bash

curl -O https://raw.githubusercontent.com/firedrakeproject/firedrake/master/scripts/firedrake-install

source /data/shared/pileus/firedrake/standard_variables

$PYTHON firedrake-install \
    --no-package-manager \
    --honour-petsc-dir \
    --mpicc=$MPICC \
    --mpicxx=$MPICXX \
    --mpif90=$MPIF90 \
    --mpiexec=$MPIEXEC \
    --venv-name=firedrake-real-opt
