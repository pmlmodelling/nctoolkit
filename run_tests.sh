
# get conda working with bash
eval "$(conda shell.bash hook)"

# set up test environment and install packages
conda create -n test_nctoolkit python=3.6 -y
conda activate test_nctoolkit
conda install pytest -y
conda install coverage -y
conda install cdo -y
conda install nco -y

pip install .



coverage run -m pytest tests/test*.py

