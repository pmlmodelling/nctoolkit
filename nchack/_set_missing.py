
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

def set_missing(self, value, silent = True):
    """Function to set the missing values"""
    """This is either a range or a single value"""

    ff = self.current

    target = tempfile.NamedTemporaryFile().name + ".nc"
    owd = os.getcwd()
   # log the full path of the file
    global nc_created
    nc_created.append(target)
    if type(value) is int:
        value = float(value)

    if type(value) is float:
        cdo_command = ("cdo setctomiss," + str(value) + " " +  ff + " " + target) 
    if type(value) is list:
        cdo_command = ("cdo setrtomiss," + str(value[0]) + "," + str(value[1]) + " " +  ff + " " + target) 


    self.history.append(cdo_command)
    run_command(cdo_command, self, silent) 
    if self.run: self.current = target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

    
