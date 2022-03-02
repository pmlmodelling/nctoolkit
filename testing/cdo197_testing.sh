eval "$(conda shell.bash hook)"
conda create -n cdo197 python=3.9 nco pytest cdo=1.9.7 -y
conda activate cdo197
pip install .

pytest tests/te*.py



