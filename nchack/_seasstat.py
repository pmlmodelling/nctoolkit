
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

def seasstat(self, stat = "mean"):
    """Function to calculate the seasonal statistic from a function""" 
    ff = self.current

    self.target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(self.target)

    cdo_command = ("cdo -seas" + stat + " " + ff + " " + self.target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self) 
    if self.run: self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def seasonal_mean(self):
    return seasstat(self, stat = "mean")

def seasonal_min(self):
    return seasstat(self, stat = "min")

def seasonal_max(self):
    return seasstat(self, stat = "max")
    
def seasonal_range(self):
    return seasstat(self, stat = "range")
