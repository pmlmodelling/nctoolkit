
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from .flatten import str_flatten
from ._depths import nc_depths 
from ._variables import variables
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runcommand import run_command

def seasstat(self, vars = None, stat = "mean"):
    """Function to calculate the seasonal statistic from a function""" 
    ff = self.current

    self.target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(self.target)

    if vars is None:
        cdo_command = ("cdo -yseas" + stat + " " + ff + " " + self.target) 
    else:
        if type(vars) is str:
            vars = [vars]
        vars_list = str_flatten(vars)
        cdo_command = ("cdo -yseas" + stat + " -selname," +  vars_list + " " + ff + " " + self.target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self) 
    if self.run: self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def seasonal_mean_climatology(self, vars = None):
    return seasstat(self, vars = vars, stat = "mean")

def seasonal_min_climatology(self, vars = None):
    return seasstat(self, vars = vars, stat = "min")

def seasonal_max_climatology(self, vars = None):
    return seasstat(self, vars = vars, stat = "max")
    
def seasonal_range_climatology(self, vars = None):
    return seasstat(self, vars = vars, stat = "range")
