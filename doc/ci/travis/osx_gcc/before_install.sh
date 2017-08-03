#!/bin/sh

set -e
brew update
# install openmpi
brew list openmpi &>/dev/null || brew install openmpi
# or install mpich2
#brew install mpich2
