from setuptools import Command, find_packages, setup


DESCRIPTION = "Efficient and intuitive tools for analyzing NetCDF data"
LONG_DESCRIPTION = """

**nctoolkit** is a comprehensive Python (3.6 and above) package for analyzing netCDF data.

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

Documentation and a user guide are available `here <https://readthedocs.org/projects/nctoolkit/>`__.

"""

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/r4ecology/nctoolkit/issues",
    "Documentation": "https://nctoolkit.readthedocs.io/en/latest",
    "Source Code": "https://github.com/r4ecology/nctoolkit",
}

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]


setup(name='nctoolkit',
      version='0.1.3',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      python_requires='>=3.6.1',
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

      project_urls=PROJECT_URLS,
      url = "https://github.com/r4ecology/nctoolkit",
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




