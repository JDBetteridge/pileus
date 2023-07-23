#!/bin/bash

git clone -c feature.manyFiles=true git@github.com:spack/spack.git

# Activate spack environment
. spack/share/spack/setup-env.sh

# Optional make an easy to reach link
ln -s $PWD/spack/share/spack/setup-env.sh $HOME/bin/

# Install something
spack install flex
