from setuptools import setup

DESCRIPTION = "Quick and efficient tools for analyzing NetCDF data"
LONG_DESCRIPTION = """
**nctoolkit** is a Python package providing easy tools for manipulating NetCDF data.

The goal of nctoolkit is to provide a comprehensive tool in Python for manipulating individual NetCDF files and ensembles of NetCDF files. The philosophy is to provide sufficient methods to carry out 80-90% of what you want to do with NetCDF files.

Under the hood, nctoolkit relies on the command line packages Climate Data Operates (CDO) and the NCO toolkit, but primarily on CDO. No prior knowledge of CDO or NCO are required to use nctoolkit. Behind the scenes, nctoolkit will generate system calls to either CDO or NCO, which are traced and can be viewed by the user. However, in almost all cases these can be ignored by most users.

The package is designed for both intensive bulk processing of NetCDF files and interactive Jupyter notebook analysis. It features an interactive plotting feature which allows users to view the contents of NetCDF files either within Jupyter notebooks or a web browser.

Documentation and a user guide are available `here <>https://readthedocs.org/projects/nctoolkit/`__.

"""

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/r4ecology/nctoolkit/issues",
    "Documentation": "https://nctoolkit.readthedocs.io/en/latest",
    "Source Code": "https://github.com/r4ecology/nctoolkit",
}

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]


setup(name='nctoolkit',
      version='0.1',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      python_requires='>=3.6.1',
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Linux",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

      project_urls=PROJECT_URLS,
      author='Robert Wilson',
      maintainer='Robert Wilson',
      author_email='rwi@pml.ac.uk',
      packages=['nctoolkit'],
      install_requires = REQUIREMENTS,
      zip_safe=False)




