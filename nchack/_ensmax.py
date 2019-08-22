
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


def ensemble_max(self, vars = None):
    """Function to calculate an ensemble max from a list of files"""
    ff_ensemble = self.current
    if type(ff_ensemble) is not list:
        raise ValueError("The current state of the tracker is not a list")
    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    owd = os.getcwd()
   # log the full path of the file
    global nc_created
    nc_created.append(self.target)

    if vars is None:
        nco_command = ("ncea -y max " + str_flatten(ff_ensemble, " ") + " " + self.target) 
    else:
        if type(vars) is str:
            vars = [vars]
        vars_list = str_flatten(vars)
        nco_command = ("ncea -y max -v " + vars_list + " " + str_flatten(ff_ensemble, " ") + " " + self.target) 


    self.history.append(nco_command)
    run_command(nco_command, self) 
    if self.run: self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

    
