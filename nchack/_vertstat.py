
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

def vertstat(self, vars = None, stat = "mean"):
    """Function to calculate the vertical mean from a function""" 
    ff = self.current

    self.target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(self.target)

    if vars is None:
        cdo_command = ("cdo -vert" + stat + " " + ff + " " + self.target) 
    else:
        if type(vars) is str:
            vars = [vars]
        vars_list = str_flatten(vars)
        cdo_command = ("cdo -vert" + stat + " -selname," +  vars_list + " " + ff + " " + self.target) 

    self.history.append(cdo_command)
    os.system(cdo_command) 
    self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def vertmean(self, vars = None):
    return vertstat(self, vars = vars, stat = "mean")

def vertmin(self, vars = None):
    return vertstat(self, vars = vars, stat = "min")

def vertmax(self, vars = None):
    return vertstat(self, vars = vars, stat = "max")
    
def vertrange(self, vars = None):
    return vertstat(self, vars = vars, stat = "range")
