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
 - name: Robert J. Wilson. Plymouth Marine Laboratory 
   index: 1
date: 25 July 2023
bibliography: paper.bib
---


# Summary

nctoolkit is a Python package for the analysis and post-processing of netCDF files. It provides a simple, intuitive interface, and includes a number of functions for common tasks such as subsetting, regridding, statistical analysis and plotting. The package is designed to be easy to use, and to require minimal code to perform common tasks. It is built on top of the Climate Data Operators (CDO)[@schulzweida_uwe_2022_7112925] library, which provides a powerful data model for working with multidimensional data. The underlying goal of the package is to provide comprehensive methods to climate, marine and atmospheric scientists working with netCDF data that will meet 80-100% of their typical processing requirements. 


# Statement of need

netCDF is a file format for storing multidimensional data, and it is the fundamental storage unit of most modelling and large-scale observational work carried out in climate, marine and atmospheric sciences. The format is self-describing, meaning that metadata is stored alongside the data, enabling computational methods to work for almost all netCDF files that follow suitable conventions. The scale and magnitude of netCDF data in use by scientists continues to grow rapdily. For example, the Coupled Model Intercomparison Project Phase 6 [@ONeill2016], produced approximately 20 PB of publicly available data [@Petrie2021]. This accumulation of data offers great opportunies to environmental scientists, however it also poses challenges because analysis software is often difficult to use by non-specialists [@Bates2018] or is inadequate. nctoolkit is a Python package that aims to fill critical gaps in the current netCDF software ecosystem. It provides a clean interface for working with netCDF files, and it has a particular focus in ensuring the compatibility of methods with oceanic model output, which often have irregular vertical grids. In contrast to other netCDF libraries, the use of CDO as a back-end allows nctoolkit users to carry out operations without having to specify the specific names of coordinates, such as longitude, latitude and time, which enables code written for one dataset to be easily applied to another. 


# Overview of Functionality 


nctoolkit's core object is the dataset, which is made up of netCDF files stored in a temporary location. Methods use the CDO library to perform operations on the dataset, and methods modify the datasets instead of returning new objects. Evaluation is lazy by default. This means that methods are only evaluated when necessary or when forced, which significantly improves performance. To ensure full functionality of nctoolkit, it is prefable that files analyzed follow the CF conventions [@Hassell2017].


The package's core functionality includes the following dataset methods: regridding (`regrid` and `to_latlon`), subsetting (`subset`), temporal statistics (`tmean`, `tmax` etc.), spatial statistics (`spatial_mean`, `spatial_max` etc.), vertical statistics and methods (`vertical_mean`, `vertical_interp`), plotting (`plot`, `pub_plot`), anomaly calculation (`annual_anomaly`), mathematical operations (`assign`) and ensemble statistics (`ensemble_mean` etc.). The package also includes a number of other methods for common tasks, including calculating the difference between two datasets(`ds1-ds2`), extracting the top layer of a dataset (`top`), and calculating the rolling mean (`rolling_mean`). The package also makes it easy to match gridded netCDF data to point observation data using the `match_points` method. 



# Example Use Case

This example shows how to calculate changes in surface temperatures projected by global climate models. The example is from the climate model MPI-ESM-2-LR under the SSP5 8.5 scenario, and we use the r1i1p1f1 variant available from the Earth System Grid Federation. We will show how to map projected changes in temperature between 1850-69 and 2080-99 and also how to calculate the global average temperature change.  The data is stored in multiple netCDF files, which are be opened using the `open_data` function. This returns a `Dataset` object, which contains the data and metadata from the netCDF file. The `Dataset` object has a number of methods for working with the data, which can be used for manipulations and analysis. In this example, we first merge the data along the time dimension. We then use the `annual_anomaly` method to calculate how much temperature will change in each model grid cell. The end of this time series, i.e. the change for 2080-99 is then mapped using `pub_plot`. Finally, we calculate the global average temperature change using the `spatial_mean` method, and plot the time series using `plot`. 

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

![Projected change in air temperature from the MPI-ESM-2-LR climate model under the SSP5 8.5 scenario. a) shows change between 1850-69 and 2080-99 per grid cell; and b) shows projected change in global average air temperature compared with 1850-69 using a rolling 20 year average.\label{fig:example}](fig.png){ width=80% }

# Development Notes

nctoolkit is developed on GitHub as an open-source package, and the authors welcome contributors and feature suggestions. We ensure the code's quality using an extensive suite of tests using the pytest module. Integration testing is carried out using GitHub Actions for both Linux and macOS. The package is tested on Python 3.8, 3.9, 3.10 and 3.11. The package is available on PyPI for Linux and macOS, and can be installed using pip. The package is also available on conda-forge for Linux, and can be installed using conda and mamba. The package is documented using Sphinx, and the documentation is hosted on ReadTheDocs. The package is licensed under the GPL-3.0 license.

 

# Acknowledgements 

This work was supported by the Natural Environment Research Council (NERC) Climate Linked Atlantic Sector Science programme (NE/R015953/1). We thank the authors of the Climate Data Operators (CDO) library for their work. In addition, nctoolkit makes use of xarray [@Hoyer2017], pandas [@mckinney2011pandas], holoviews [@Stevens2015] and matplotlib [@hunter2007matplotlib] for the core plotting functionality. COBE Sea Surface Temperature data provided by the NOAA PSL, Boulder, Colorado, USA, from their website at [https://psl.noaa.gov](https://psl.noaa.gov).

