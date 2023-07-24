#!/bin/bash

# Update the system
sudo apt-get update
sudo apt-get upgrade

# Install Firedrake packages
# Check
# https://github.com/firedrakeproject/firedrake/blob/master/docker/Dockerfile.env
# for updates
sudo apt-get install curl \
     openssh-client build-essential autoconf automake \
     cmake gfortran git libopenblas-serial-dev \
     libtool python3-dev python3-pip python3-tk python3-venv \
     python3-requests zlib1g-dev libboost-dev sudo gmsh \
     bison flex \
     liboce-ocaf-dev \
     swig graphviz \
     libcurl4-openssl-dev libxml2-dev

# Editors
sudo apt-get install emacs vim

# XTerm for parallel debugging
sudo apt-get install xterm