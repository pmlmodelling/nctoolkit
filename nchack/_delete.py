
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command


def remove_variable(self, vars):
    """Function to select the season"""

    self.target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)

    if type(vars) is not list:
        vars = [vars]
    vars = str_flatten(vars, ",")
    
    cdo_command = "cdo delete,name=" + vars + " " + self.current + " " + self.target
    self.history.append(cdo_command)
    run_command(cdo_command, self)
    
    if self.run: self.current = self.target 
    
    cleanup(keep = self.current)
    
    return(self)


