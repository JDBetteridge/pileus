#!/bin/bash

. spack/share/spack/setup-env.sh

# Flex is missing on the system
spack install flex

# The installed GCC is missing gfortran
spack install gcc@13.1

# CMake is not installed
spack install cmake

# System Python is 3.8, which is end-of-life next year (2024)
spack install python@3.11
