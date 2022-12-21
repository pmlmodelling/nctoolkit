#!/bin/bash -e
# modified from https://raw.githubusercontent.com/nctoolkit-dev/pandas/main/.circleci/setup_env.sh

echo "Install Mambaforge"
MAMBA_URL="https://github.com/conda-forge/miniforge/releases/download/4.14.0-0/Mambaforge-4.14.0-0-Linux-aarch64.sh"
echo "Downloading $MAMBA_URL"
wget -q $MAMBA_URL -O minimamba.sh
chmod +x minimamba.sh

MAMBA_DIR="$HOME/miniconda3"
rm -rf $MAMBA_DIR
./minimamba.sh -b -p $MAMBA_DIR

export PATH=$MAMBA_DIR/bin:$PATH

echo
echo "which conda"
which conda

echo
echo "update conda"
conda config --set ssl_verify false
conda config --set quiet true --set always_yes true --set changeps1 false
mamba install -y -c conda-forge -n base pip setuptools

echo "conda info -a"
conda info -a

echo "conda list (root environment)"
conda list

echo
# Clean up any left-over from a previous build
mamba env remove -n nctoolkit-dev
echo "mamba env update --file=${ENV_FILE}"
# See https://github.com/mamba-org/mamba/issues/633
mamba create -q -n nctoolkit-dev
time mamba env update -n nctoolkit-dev --file="${ENV_FILE}"

echo "activate nctoolkit-dev"
source activate nctoolkit-dev

mamba install cdo nco cartopy -y
