eval "$(conda shell.bash hook)"
conda create -n cdo198 python=3.9 nco pytest cdo=1.9.8 -y
conda activate cdo198
pip install .

pytest tests/te*.py



