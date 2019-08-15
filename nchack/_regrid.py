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

def regrid(self, vars = None, grid = None, method = "bil", weights_file = None):

    grid_type = None

    # find the grid type
    if isinstance(grid, pd.DataFrame):
        grid_type = "df"

    # If the grid is an xarray object, we need to convert it to .nc
    if isinstance(grid, xr.Dataset):
        grid_type = "xr"
        temp_nc = tempfile.NamedTemporaryFile().name + ".nc"
        nc_created.append(temp_nc)
        grid.to_netcdf(temp_nc)
        grid = temp_nc

    if type(grid) is str:
        if os.path.exists(grid) == False:
            raise ValueError("grid file supplied does not exist")
        if grid.endswith(".nc") == False:
            raise ValueError("grid file supplied is not a netcdf file!")
        grid_type = "nc"

    if grid_type is None:
        raise ValueError("grid supplied is not valid")

   # log the full path of the file
    ##ff_orig = os.path.abspath(self.current)

    # need a check at this point for file validity     
    holding_nc = self.current 
    self.target  = tempfile.NamedTemporaryFile().name + ".nc"
    temp_nc = tempfile.NamedTemporaryFile().name + ".nc"
    dummy_nc = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    nc_created.append(temp_nc)
    nc_created.append(dummy_nc)
     # check if variables are included
     # first, a hack to make sure vars is something we can iterate over
    if vars != None:
        if type(vars) is str:
            vars = {vars}
    
    if (vars is None) == False:
        ff_variables = self.variables()
        for vv in vars:
             if (vv in ff_variables) == False:
                 raise ValueError("variable " + vv + " is not available in the netcdf file")
    # check that the remapping method is valid
    if (method in {"bil", "dis", "nn"}) == False:
        raise ValueError("remapping method is invalid. Please check")
     
     # need code at this point to add missing grid if it's needed
     
     # same with na_value stuff. But maybe that isn't really needed
     # a distraction?
     
     # check the number of grids in the file

    if vars != None:
        cdo_call = ("cdo selname," + str_flatten(vars) + " " + holding_nc + " " + dummy_nc)
        self.history.append(cdo_call)
        run_command(cdo_call)
        if holding_nc == self.current:
           holding_nc = temp_nc
      # throw error if selecting vars fails
        if os.path.isfile(dummy_nc) == False:
           raise ValueError("variable selection did not work. Check output")
        os.rename(dummy_nc, holding_nc)
    # Do do the horizontal regridding
   
    if grid is not None:
                   # first generate the grid
        if self.grid is None:
            if grid_type == "df":
                self.grid = generate_grid(grid)
                nc_created.append(self.grid)
            else:
                self.grid = grid
            
        # first we need to generate the weights for remapping
        # and add this to the files created list and self.weights
        if self.weights is None:
            weights_nc = tempfile.NamedTemporaryFile().name + ".nc"
            nc_created.append(weights_nc)
            self.weights = weights_nc
            
            weights_nc = self.weights

            cdo_call = ("cdo gen" + method + ","+ self.grid+ " " + holding_nc + " " + weights_nc)
            self.history.append(cdo_call)
            run_command(cdo_call)
        else:
            weights_nc = self.weights

        cdo_call = ("cdo remap," + self.grid + "," + weights_nc +  " " + holding_nc + " " + dummy_nc)
        self.history.append(cdo_call)
        run_command(cdo_call)
        if os.path.isfile(dummy_nc) == False:
            raise ValueError("horizontal remapping did not work. Check output")
   
        if holding_nc == self.current:
            holding_nc = temp_nc

        os.rename(dummy_nc, holding_nc)
        
    os.rename(holding_nc, self.target)

    self.current = self.target 

    cleanup(keep = [self.current, self.weights, self.grid])

    return(self)

