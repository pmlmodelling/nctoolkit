from setuptools import setup
import subprocess

# check version of cdo installed


cdo_check = subprocess.run("which cdo", shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cdo_check = str(cdo_check.stdout).replace("\\n", "")
cdo_check = cdo_check.replace("b'", "").strip()
if len(cdo_check) < 2:
    print("Please install cdo")

cdo_check = subprocess.run("cdo --version", shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
cdo_check = str(cdo_check.stderr).replace("\\n", "")
cdo_check = cdo_check.replace("b'", "").strip()
cdo_version = cdo_check.split("(")[0].strip().split(" ")[-1]
#if cdo_version not in ["1.9.8"]:
#    raise ValueError("Please install cdo version 1.9.8 or above")

setup(name='nctoolkit',
      version='0.1',
      description='A general purpose python tool for manipulating, analyzing and plotting data from netcdf files',
      url='https://readthedocs.org/projects/nchack/',
      author='Robert Wilson',
      author_email='rwi@pml.ac.uk',
      license='MIT',
      packages=['nctoolkit'],
      install_requires=['xarray','netcdf4', "dask[complete]", "hvplot", "panel", "bokeh"],
      zip_safe=False)




