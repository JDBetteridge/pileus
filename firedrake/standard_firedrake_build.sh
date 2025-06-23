#!/bin/bash
set -x

source /data/shared/pileus/firedrake/standard_variables

# Create the virtualenv
VENV_NAME=${VENV_NAME:-firedrake-real-opt}
$PYTHON -m venv $VENV_NAME
source ./$VENV_NAME/bin/activate

# Install Firedrake
pip cache remove petsc4py
pip cache remove slepc4py
pip cache remove firedrake
env CC=$MPICC CXX=$MPICXX pip install --no-binary h5py 'firedrake[check,vtk,slepc]'

# Clone and install Gusto
mkdir -p ./$VENV_NAME/src
cd ./$VENV_NAME/src
git clone https://github.com/firedrakeproject/gusto.git
pip install -e ./gusto
