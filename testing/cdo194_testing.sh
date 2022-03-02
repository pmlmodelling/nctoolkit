eval "$(conda shell.bash hook)"
conda create -n cdo197 python=3.9 nco pytest -y
conda activate cdo197
bash cdo_installers/cdo194_install.sh
pip install .

pytest tests/te*.py



