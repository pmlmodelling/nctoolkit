
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

def time_stat(self, vars = None, stat = "mean"):
    """Function to calculate the mean from from a single file"""
    ff = self.current

    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    owd = os.getcwd()
   # log the full path of the file
    global nc_created
    nc_created.append(self.target)

    if vars is None:
        cdo_command = ("cdo tim" + stat + " " + ff + " " + self.target) 
    else:
        if type(vars) is str:
            vars = [vars]
        vars_list = str_flatten(vars)
        cdo_command = ("cdo -tim" + stat + " -selname," + vars_list + " " + ff + " " + self.target) 


    self.history.append(cdo_command)
    run_command(cdo_command, self) 
    if self.run: self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def time_mean(self, vars = None):
    return(time_stat(self, vars = vars, stat = "mean"))

def time_min(self, vars = None):
    return(time_stat(self, vars = vars, stat = "min"))

def time_max(self, vars = None):
    return(time_stat(self, vars = vars, stat = "max"))


def time_range(self, vars = None):
    return(time_stat(self, vars = vars, stat = "range"))

def time_var(self, vars = None):
    return(time_stat(self, vars = vars, stat = "var"))





    
