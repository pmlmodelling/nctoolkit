
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

def vertstat(self, stat = "mean"):
    """Function to calculate the vertical mean from a function""" 
    ff = self.current

    self.target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(self.target)

    cdo_command = ("cdo -vert" + stat + " " + ff + " " + self.target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self) 
    if self.run: self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def vertical_mean(self):
    return vertstat(self, stat = "mean")

def vertical_min(self):
    return vertstat(self, stat = "min")

def vertical_max(self):
    return vertstat(self, stat = "max")
    
def vertical_range(self):
    return vertstat(self, stat = "range")
