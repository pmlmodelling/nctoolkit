import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._generate_grid import generate_grid
from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command

def rename(self, newnames):
    """Function to rename netcdf variable"""

    if type(newnames) is not dict:
        raise ValueError("a dictionary was not supplied")

    # now, we need to loop through the renaming dictionary to get the cdo sub
    cdo_rename = ""
    
    for key, value in newnames.items():
        cdo_rename +=  "," + key
        cdo_rename += "," + value

    # need a check at this point for file validity     
    self.target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    cdo_call = ("cdo chname" + cdo_rename + " " + self.current + " " + self.target)
    self.history.append(cdo_call)
    run_command(cdo_call)
        

    self.current = self.target 

    cleanup(keep = self.current)

    return(self)

