
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

def ensemble_mean(self, vars = None, check = False):
    """Function to calculate an ensemble mean from a list of files"""
    ff_ensemble = self.current
    if type(ff_ensemble) is not list:
        raise ValueError("The current state of the tracker is not a list")
    
    if check:
        all_grid = []
        for ff in self.current:
            all_grid.append("cdo griddes " + ff)
        if len(set(all_grid)) > 1:
            raise ValueError("grids are incompatible")

    if check:
        all_names = []
        for ff in self.current:
            all_names.append("cdo showname " + ff)
        if len(set(all_grid)) > 1:
            raise ValueError("Files have different variables")

    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    owd = os.getcwd()
   # log the full path of the file
    global nc_created
    nc_created.append(self.target)

    if vars is None:
        nco_command = ("ncea -y mean " + str_flatten(ff_ensemble, " ") + " " + self.target) 
    else:
        if type(vars) is str:
            vars = [vars]
        vars_list = str_flatten(vars)
        nco_command = ("ncea -y mean -v " + vars_list + " " + str_flatten(ff_ensemble, " ") + " " + self.target) 


    self.history.append(nco_command)
    run_command(nco_command, self) 
    if self.run: self.current = self.target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

    
