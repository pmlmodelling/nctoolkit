
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

def monstat(self,  stat = "mean"):
    """Function to calculate the monthly statistic from a netcdf file""" 
    ff = self.current

    self.target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(self.target)

    cdo_command = ("cdo -mon" + stat + " " + ff + " " + self.target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self) 
    if self.run: self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def monthly_mean(self):
    return monstat(self, stat = "mean")

def monthly_min(self):
    return monstat(self, stat = "min")

def monthly_max(self):
    return monstat(self, stat = "max")
    
def monthly_range(self):
    return monstat(self, stat = "range")
