eval "$(conda shell.bash hook)"
conda create -n cdo196 python=3.9 nco pytest cdo=1.9.6 -y
conda activate cdo196
pip install .

pytest tests/te*.py



