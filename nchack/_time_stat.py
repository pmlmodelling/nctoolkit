
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

def time_stat(self, stat = "mean"):
    """Function to calculate the mean from from a single file"""
    ff = self.current

    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    owd = os.getcwd()
   # log the full path of the file
    global nc_created
    nc_created.append(self.target)

    cdo_command = ("cdo --reduce_dim tim" + stat + " " + ff + " " + self.target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self) 
    if self.run: self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def time_mean(self):
    return(time_stat(self, stat = "mean"))

def time_min(self):
    return(time_stat(self, stat = "min"))

def time_max(self):
    return(time_stat(self, stat = "max"))


def time_range(self):
    return(time_stat(self,jstat = "range"))

def time_var(self):
    return(time_stat(self, stat = "var"))





    
