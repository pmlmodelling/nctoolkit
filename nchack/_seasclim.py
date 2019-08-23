
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

def seasstat(self, stat = "mean", silent = True):
    """Function to calculate the seasonal statistic from a function""" 
    ff = self.current

    target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(target)

    cdo_command = ("cdo -yseas" + stat + " " + ff + " " + target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self, silent) 
    if self.run: self.current = target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def seasonal_mean_climatology(self, silent = True):
    return seasstat(self, stat = "mean", silent = True)

def seasonal_min_climatology(self, silent = True):
    return seasstat(self, stat = "min", silent = True)

def seasonal_max_climatology(self, silent = True):
    return seasstat(self, stat = "max", silent = True)
    
def seasonal_range_climatology(self, silent = True):
    return seasstat(self, stat = "range", silent = True)
