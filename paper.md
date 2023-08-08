---
title: 
  'nctoolkit: A Python package for netCDF analysis and post-processing'
tags:
  - Python
  - climate
  - netCDF
authors:
  - name: Robert J. Wilson 
    orcid: 0000-0002-0592-366X 
    equal-contrib: false
    affiliation: "1" # (Multiple affiliations must be quoted)
    corresponding: true # (This is how to denote the corresponding author)

  - name: Yuri Artioli
    orcid: 0000-0002-5498-4223 
    affiliation: "1" # (Multiple affiliations must be quoted)

affiliations:
 - name: Plymouth Marine Laboratory, The Hoe, Plymouth, UK
   index: 1
date: 25 July 2023
bibliography: paper.bib
---


# Summary

nctoolkit is a Python package for the analysis and post-processing of netCDF files. It provides a simple, intuitive interface, and includes methods for common tasks such as subsetting, regridding, statistical analysis and plotting. The package is designed to be easy to use, and to require minimal code for performing common tasks. It is built on top of the Climate Data Operators (CDO) library [@schulzweida_uwe_2022_7112925], which provides a powerful data model for working with multidimensional data. The core aim of the package is to provide over 80% of the typical data processing requirements for climate, marine and atmospheric scientists who work with netCDF data. 


# Statement of need

netCDF is a file format for storing multidimensional data, and it is the fundamental storage unit for most modelling and large-scale observational work carried out in climate, marine and atmospheric science. Files typically represent spatiotemporal data, such as atmospheric or oceanic temperatures. In contrast to other data formats, such as csv, netCDF files are self-describing and typically follow universally agreed conventions for coordinate names and file structure etc. As a result, it is possible to write software that can work with almost all netCDF files that follow these conventions, and there is no automatic need to burden users with the task of identifying the names given to coordinates, such as time, within the files themselves. Software can therefore be written that will carry out operations, such as calculating spatial averages, in one line of code that might otherwise require users to write multiple lines of code, and for these operations to largely work on any netCDF file.

The scale of netCDF data in use by scientists continues to grow rapidly. For example, the Coupled Model Intercomparison Project Phase 6 [@ONeill2016], produced approximately 20 petabytes of publicly available climate model data [@Petrie2021]. This accumulation of data offers great opportunities to environmental scientists. However, it also poses challenges because analysis software is often difficult to use by non-specialists [@Bates2018] or is inadequate. nctoolkit is a Python package that aims to fill critical gaps in the current netCDF software ecosystem. It provides a clean interface for working with netCDF files, and it has a particular focus in ensuring the compatibility of methods with oceanic model output, which often have irregular vertical grids. 

The nctoolkit package sits within a Python ecosystem of packages such as xarray and iris, which provide data models and analysis software for netCDF, and netCDF4 which provides low level access to netCDF data. This ecosystem also includes specialist software such as xesmf for processes such as regridding and cf-xarray which makes xarray more format-agnostic. In contrast to other netCDF libraries, the use of CDO as a back-end allows nctoolkit users to carry out operations, such as spatial averages, without having to specify the specific names of coordinates, such as longitude, latitude and time, which enables code written for one dataset to be easily applied to another. 


# Overview of Functionality 


nctoolkit's core object is a `Dataset`, which is made up of netCDF files stored in a temporary location. Methods use the CDO library to perform operations on a `Dataset`, and they modify a `Dataset` instead of returning a new object. Evaluation is lazy by default. This means that methods are only evaluated when necessary or when forced, which significantly improves performance. To ensure full functionality of nctoolkit, it is preferable that files follow the CF conventions [@Hassell2017].


The package's core functionality includes the following `Dataset` methods: regridding (`regrid` and `to_latlon`), subsetting (`subset`), temporal statistics (`tmean`, `tmax` etc.), spatial statistics (`spatial_mean`, `spatial_max` etc.), vertical statistics and methods (`vertical_mean`, `vertical_interp`), plotting (`plot`, `pub_plot`), anomaly calculation (`annual_anomaly`), mathematical operations (`assign`) and ensemble statistics (`ensemble_mean` etc.). The package also includes a range of methods for common tasks, including calculating the difference between one `Dataset` and another (`ds1-ds2`), extracting the top and bottom layers of a `Dataset` (`top` and `bottom`), and calculating the rolling mean (`rolling_mean`). The package also makes it easy to match gridded netCDF data to point observation data using the `match_points` method. A `Dataset` can use multiple files as input, and the `multiprocessing` package is used internally by nctoolkit to enable easy parallelization of operations on multiple files.



# Example Use Case

This example shows how to calculate how much a climate model projects global surface temperatures to change. The example is from the climate model MPI-ESM-2-LR [@mauritsen2019developments] under the SSP5 8.5 climate change scenario, and we use the r1i1p1f1 variant. This data is downloadable from the Earth System Grid Federation and is made available on Zenodo: [10.5281/zenodo.8182678](https://zenodo.org/record/8182678).
 
We will show how to map projected changes in temperature between 1850-69 and 2080-99 and also how to calculate a time series of global average temperature change. The data is stored in multiple netCDF files, which are opened using the `open_data` function. This returns a `Dataset` object, which contains the data and metadata from the netCDF file. The `Dataset` object has a number of methods for working with the data, which can be used for manipulation and analysis. In this example, we first merge the data along the time dimension. We then use the `annual_anomaly` method to calculate how much temperature will change in each model grid cell. The end of this time series, i.e., the change for 2080-99 is then mapped using `pub_plot`. Finally, we calculate the global average temperature change using the `spatial_mean` method and plot the time series using `plot`. 

```python

import nctoolkit as nc

ds_ts = nc.open_data("*.nc")

ds_ts.merge("time")

ds_ts.annual_anomaly(baseline = [1850, 1869], window = 20)

ds_end = ds_ts.copy()

ds_end.subset(time = -1)

ds_end.pub_plot()

ds_global = ds_ts.copy()

ds_global.spatial_mean()

ds_global.plot()

```

![Projected changes in air temperature from the MPI-ESM-2-LR climate model under the SSP5 8.5 scenario. a) shows changes in the 20-year average between 1850-69 and 2080-99 in each model grid cell; and b) shows projected change in global average air temperature compared with 1850-69 using a rolling 20-year average.\label{fig:example}](fig.png){ width=80% }

# Development Notes

nctoolkit is developed on GitHub as an open-source package, and the authors welcome contributions and feature suggestions. We ensure the code's quality with an extensive suite of tests using the pytest package. Continuous Integration testing is carried out using GitHub Actions for both Linux and macOS. The package is tested on Python 3.8, 3.9, 3.10 and 3.11. It is available on PyPI and conda-forge for Linux and macOS, and can be installed using pip, conda and mamba. The package is documented using Sphinx, and the documentation is hosted on Read the Docs. It is licensed under the GPL-3.0 license.

 

# Acknowledgements 

This work was supported by the Natural Environment Research Council (NERC) Climate Linked Atlantic Sector Science programme (NE/R015953/1). We thank the authors of the Climate Data Operators (CDO) library for their work. In addition, nctoolkit makes use of xarray [@Hoyer2017], pandas [@mckinney2011pandas], holoviews [@Stevens2015] and matplotlib [@hunter2007matplotlib] for the core plotting functionality. We acknowledge the World Climate Research Programme, which, through its Working Group on Coupled Modelling, coordinated and promoted CMIP6.

# References 

