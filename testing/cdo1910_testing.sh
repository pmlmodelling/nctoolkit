eval "$(conda shell.bash hook)"
conda create -n cdo1910 python=3.9 nco pytest cdo=1.9.10 -y
conda activate cdo1910
pip install .

pytest tests/te*.py



