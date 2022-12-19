from setuptools import Command, find_packages, setup
import sys

DESCRIPTION = "Fast and easy analysis of netCDF data in Python"
LONG_DESCRIPTION = """

**nctoolkit** is a comprehensive Python (3.6 and above) package for analyzing netCDF data on Linux and macOS.

Core abilities of nctoolkit include:

  - Clipping to spatial regions
  - Calculating climatologies
  - Subsetting to specific time periods
  - Calculating spatial statistics
  - Creating new variables using arithmetic operations
  - Calculating anomalies
  - Calculating rolling and cumulative statistics
  - Horizontally and vertically remapping data
  - Calculating time averages
  - Interactive plotting of data
  - Calculating the correlations between variables
  - Calculating vertical statistics for the likes of oceanic data
  - Calculating ensemble statistics
  - Calculating phenological metrics

Operation of the package requires the installation of Climate Data Operators (CDO). This is the computational backend for most of the methods used. No knowledge of CDO is required to use nctoolkit. A couple of methods provide users with the option of using netCDF Operators (NCO) as a backend. Guidance for how to install the backends are available `here <https://nctoolkit.readthedocs.io/en/stable/installing.html>`__.

The package is designed for both intensive bulk processing of NetCDF files and interactive Jupyter notebook analysis. It features an interactive plotting feature which allows users to view the contents of NetCDF files either within Jupyter notebooks or a web browser.

Plotting requires the use of cartopy, which has some additional system dependencies. Follow the instructions `here <https://scitools.org.uk/cartopy/docs/latest/installing.html>`__ to install them.

Documentation and a user guide are available `here <https://nctoolkit.readthedocs.io/en/stable>`__.

"""

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/pmlmodelling/nctoolkit/issues",
    "Documentation": "https://nctoolkit.readthedocs.io/en/stable",
    "Source Code": "https://github.com/pmlmodelling/nctoolkit",
}

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(name='nctoolkit',
      version='0.8.6',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      python_requires='>=3.6.1',
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

      project_urls=PROJECT_URLS,
      url = "https://github.com/pmlmodelling/nctoolkit",
      author='Robert Wilson',
      maintainer='Robert Wilson',
      author_email='rwi@pml.ac.uk',

      packages = ["nctoolkit"],
      setup_requires=[
        'setuptools',
        'setuptools-git',
        'wheel',
    ],
      install_requires = REQUIREMENTS,
      zip_safe=False)




