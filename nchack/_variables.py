
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

# function to get list of variables

def variables(self, detailed = False):
    cdo_result = os.popen( "cdo showname " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
  #  if detailed == False:
    return(cdo_result)
