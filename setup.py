from setuptools import setup

setup(name='nchack',
      version='0.1',
      description='A general purpose python tool for manipulating, analyzing and plotting data from netcdf files',
      url='https://readthedocs.org/projects/nchack/',
      author='Robert Wilson',
      author_email='rwi@pml.ac.uk',
      license='MIT',
      packages=['nchack'],
      install_requires=['xarray','netcdf4','hvplot', "dask", "pyviz"],
      zip_safe=False)




