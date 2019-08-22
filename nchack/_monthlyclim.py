
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

def ymonstat(self, stat = "mean"):
    """Function to calculate the seasonal statistic from a function""" 
    ff = self.current

    self.target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(self.target)

    cdo_command = ("cdo -ymon" + stat + " " + ff + " " + self.target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self) 
    if self.run: self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def monthly_mean_climatology(self):
    return ymonstat(self, stat = "mean")

def monthly_min_climatology(self):
    return ymonstat(self, stat = "min")

def monthly_max_climatology(self):
    return ymonstat(self,  stat = "max")
    
def monthly_range_climatology(self):
    return ymonstat(self, stat = "range")
