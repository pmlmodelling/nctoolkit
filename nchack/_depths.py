
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools
# function to get the depths available in a netcdf file

def nc_depths(ff):
    cdo_result = os.popen( "cdo showlevel " + ff).read()
    cdo_result = cdo_result.replace("\n", "").split()
    cdo_result = pd.Series( (float(v) for v in cdo_result) )
    cdo_result = pd.Series.unique(cdo_result)
    return(cdo_result)
