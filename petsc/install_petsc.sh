#!/bin/bash

BASE_INSTALL_DIR=$PWD
MAKE_NP=32 # Use up to 32 cores when building

git clone https://github.com/firedrakeproject/petsc.git
git clone https://github.com/firedrakeproject/slepc.git

####################
# Part 1: Packages #
####################

# Build MPICH and all required packages
cd petsc
./configure \
    --COPTFLAGS=-O3 -march=native -mtune=native \
    --CXXOPTFLAGS=-O3 -march=native -mtune=native \
    --FOPTFLAGS=-O3 -march=native -mtune=native \
    --with-c2html=0 \
    --with-debugging=0 \
    --with-fortran-bindings=0 \
    --with-make-np=$MAKE_NP \
    --with-shared-libraries=1 \
    --with-zlib \
    --download-chaco \
    --download-fftw \
    --download-hdf5 \
    --download-hwloc \
    --download-hypre \
    --download-metis \
    --download-ml \
    --download-mumps \
    --download-mpich \
    --download-mpich-device=ch3:sock \
    --download-netcdf \
    --download-openblas \
    --download-pastix \
    --download-pnetcdf \
    --download-ptscotch \
    --download-scalapack \
    --download-suitesparse \
    --download-superlu_dist \
    PETSC_ARCH=packages
# Don't run make here, we only want MPICH and HWLOC
# It is also necessary to move `petscconf.h` so packages isn't treated like a working PETSc
mv packages/include/petscconf.h packages/include/old_petscconf.nope


####################
# Part 2: Real     #
####################

# Build real debug Firedrake PETSc
export PACKAGES=$BASE_INSTALL_DIR/petsc/packages; \
./configure \
    --with-c2html=0 \
    --with-debugging=1 \
    --with-fortran-bindings=0 \
    --with-make-np=$MAKE_NP \
    --with-shared-libraries=1 \
    --with-bison \
    --with-flex \
    --with-zlib \
    --with-blas-dir=$PACKAGES \
    --with-chaco-dir=$PACKAGES \
    --with-fftw-dir=$PACKAGES \
    --with-hdf5-dir=$PACKAGES \
    --with-hwloc-dir=$PACKAGES \
    --with-hypre-dir=$PACKAGES \
    --with-metis-dir=$PACKAGES \
    --with-ml-dir=$PACKAGES \
    --with-mpi-dir=$PACKAGES \
    --with-mumps-dir=$PACKAGES \
    --with-netcdf-dir=$PACKAGES \
    --with-pastix-dir=$PACKAGES \
    --with-pnetcdf-dir=$PACKAGES \
    --with-ptscotch-dir=$PACKAGES \
    --with-scalapack-dir=$PACKAGES \
    --with-suitesparse-dir=$PACKAGES \
    --with-superlu_dist-dir=$PACKAGES \
    PETSC_ARCH=real-debug
make PETSC_DIR=$BASE_INSTALL_DIR/petsc PETSC_ARCH=real-debug all

# Build real debug Firedrake SLEPc
export PETSC_DIR=$BASE_INSTALL_DIR/petsc
export PETSC_ARCH=real-debug
cd $BASE_INSTALL_DIR/slepc
./configure
make SLEPC_DIR=$BASE_INSTALL_DIR/slepc PETSC_DIR=$BASE_INSTALL_DIR/petsc PETSC_ARCH=real-debug
unset PETSC_DIR

# Build real optimised Firedrake PETSc
export PACKAGES=$BASE_INSTALL_DIR/petsc/packages; \
./configure \
    --COPTFLAGS=-O3 -march=native -mtune=native \
    --CXXOPTFLAGS=-O3 -march=native -mtune=native \
    --FOPTFLAGS=-O3 -march=native -mtune=native \
    --with-c2html=0 \
    --with-debugging=0 \
    --with-fortran-bindings=0 \
    --with-make-np=$MAKE_NP \
    --with-shared-libraries=1 \
    --with-bison \
    --with-flex \
    --with-zlib \
    --with-blas-dir=$PACKAGES \
    --with-chaco-dir=$PACKAGES \
    --with-fftw-dir=$PACKAGES \
    --with-hdf5-dir=$PACKAGES \
    --with-hwloc-dir=$PACKAGES \
    --with-hypre-dir=$PACKAGES \
    --with-metis-dir=$PACKAGES \
    --with-ml-dir=$PACKAGES \
    --with-mpi-dir=$PACKAGES \
    --with-mumps-dir=$PACKAGES \
    --with-netcdf-dir=$PACKAGES \
    --with-pastix-dir=$PACKAGES \
    --with-pnetcdf-dir=$PACKAGES \
    --with-ptscotch-dir=$PACKAGES \
    --with-scalapack-dir=$PACKAGES \
    --with-suitesparse-dir=$PACKAGES \
    --with-superlu_dist-dir=$PACKAGES \
    PETSC_ARCH=real-opt
make PETSC_DIR=$BASE_INSTALL_DIR/petsc PETSC_ARCH=real-opt all

# Build real optimised Firedrake SLEPc
export PETSC_DIR=$BASE_INSTALL_DIR/petsc
export PETSC_ARCH=real-opt
cd $BASE_INSTALL_DIR/slepc
./configure
make SLEPC_DIR=$BASE_INSTALL_DIR/slepc PETSC_DIR=$BASE_INSTALL_DIR/petsc PETSC_ARCH=real-opt
unset PETSC_DIR


####################
# Part 3: Complex  #
####################

# Build complex debug PETSc for Firedrake
cd $BASE_INSTALL_DIR/petsc
./configure \
    --with-c2html=0 \
    --with-debugging=1 \
    --with-fortran-bindings=0 \
    --with-make-np=$MAKE_NP \
    --with-scalar-type=complex \
    --with-shared-libraries=1 \
    --with-bison \
    --with-flex \
    --with-zlib \
    --with-blas-dir=$PACKAGES \
    --with-chaco-dir=$PACKAGES \
    --with-fftw-dir=$PACKAGES \
    --with-hdf5-dir=$PACKAGES \
    --with-hwloc-dir=$PACKAGES \
    --with-metis-dir=$PACKAGES \
    --with-mpi-dir=$PACKAGES \
    --with-mumps-dir=$PACKAGES \
    --with-netcdf-dir=$PACKAGES \
    --with-pastix-dir=$PACKAGES \
    --with-pnetcdf-dir=$PACKAGES \
    --with-ptscotch-dir=$PACKAGES \
    --with-scalapack-dir=$PACKAGES \
    --with-suitesparse-dir=$PACKAGES \
    --with-superlu_dist-dir=$PACKAGES \
    PETSC_ARCH=complex-debug
make PETSC_DIR=$BASE_INSTALL_DIR/petsc PETSC_ARCH=complex-debug all

# Build complex debug Firedrake SLEPc
export PETSC_DIR=$BASE_INSTALL_DIR/petsc
export PETSC_ARCH=complex-debug
cd $BASE_INSTALL_DIR/slepc
./configure
make SLEPC_DIR=$BASE_INSTALL_DIR/slepc PETSC_DIR=$BASE_INSTALL_DIR/petsc PETSC_ARCH=complex-debug

# Build complex optimised PETSc for Firedrake
cd $BASE_INSTALL_DIR/petsc
./configure \
    --COPTFLAGS=-O3 -march=native -mtune=native \
    --CXXOPTFLAGS=-O3 -march=native -mtune=native \
    --FOPTFLAGS=-O3 -march=native -mtune=native \
    --with-c2html=0 \
    --with-debugging=1 \
    --with-fortran-bindings=0 \
    --with-make-np=$MAKE_NP \
    --with-scalar-type=complex \
    --with-shared-libraries=1 \
    --with-bison \
    --with-flex \
    --with-zlib \
    --with-blas-dir=$PACKAGES \
    --with-chaco-dir=$PACKAGES \
    --with-fftw-dir=$PACKAGES \
    --with-hdf5-dir=$PACKAGES \
    --with-hwloc-dir=$PACKAGES \
    --with-metis-dir=$PACKAGES \
    --with-mpi-dir=$PACKAGES \
    --with-mumps-dir=$PACKAGES \
    --with-netcdf-dir=$PACKAGES \
    --with-pastix-dir=$PACKAGES \
    --with-pnetcdf-dir=$PACKAGES \
    --with-ptscotch-dir=$PACKAGES \
    --with-scalapack-dir=$PACKAGES \
    --with-suitesparse-dir=$PACKAGES \
    --with-superlu_dist-dir=$PACKAGES \
    PETSC_ARCH=complex-opt
make PETSC_DIR=$BASE_INSTALL_DIR/petsc PETSC_ARCH=complex-opt all

# Build complex optimised Firedrake SLEPc
export PETSC_DIR=$BASE_INSTALL_DIR/petsc
export PETSC_ARCH=complex-opt
cd $BASE_INSTALL_DIR/slepc
./configure
make SLEPC_DIR=$BASE_INSTALL_DIR/slepc PETSC_DIR=$BASE_INSTALL_DIR/petsc PETSC_ARCH=complex-opt

# Set some useful environment variables
# PETSC_DIR /home/firedrake/petsc
# SLEPC_DIR /home/firedrake/slepc
# MPICH_DIR /home/firedrake/petsc/packages/bin
# HDF5_DIR /home/firedrake/petsc/packages
# HDF5_MPI ON
# OMP_NUM_THREADS 1
# OPENBLAS_NUM_THREADS 1
