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

def regrid(self, grid = None, method = "bil", silent = True):

    if grid is None:
        raise ValueError("No grid was supplied")

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
    target  = tempfile.NamedTemporaryFile().name + ".nc"
    temp_nc = tempfile.NamedTemporaryFile().name + ".nc"
    dummy_nc = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)
    nc_created.append(temp_nc)
    nc_created.append(dummy_nc)

    # check that the remapping method is valid
    if (method in {"bil", "dis", "nn"}) == False:
        raise ValueError("remapping method is invalid. Please check")
     
     # need code at this point to add missing grid if it's needed
     
     # same with na_value stuff. But maybe that isn't really needed
     # a distraction?
     
     # check the number of grids in the file

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

            cdo_command = ("cdo gen" + method + ","+ self.grid+ " " + holding_nc + " " + weights_nc)
            self.history.append(cdo_command)
            run_command(cdo_command, self, silent)
        else:
            weights_nc = self.weights

        cdo_command= ("cdo remap," + self.grid + "," + weights_nc +  " " + holding_nc + " " + dummy_nc)
        self.history.append(cdo_command)
        run_command(cdo_command, self, silent)
   
        if holding_nc == self.current:
            holding_nc = temp_nc

        os.rename(dummy_nc, holding_nc)
        
    os.rename(holding_nc, target)

    if self.run: self.current = target 

    cleanup(keep = [self.current, self.weights, self.grid])

    return(self)

