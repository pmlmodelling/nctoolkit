import os
import xarray as xr
import pandas as pd

from ._temp_file import temp_file
from ._api import open_data

from ._generate_grid import generate_grid
from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._filetracker import nc_safe
from ._runthis import run_this

def regrid(self, grid = None, method = "bil", cores = 1):

    """
    Regrid a tracker for a target grid and remapping method

    Parameters
    -------------
    grid : nchack.tracker, xarray obect, pandas data frame or netcdf file 
        grid to remap to 
    method : str
        remapping method. Defaults to "bil". Bilinear: "bil"; Nearest neighbour: "nn",....
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.DataSet
        Reduced tracker with the regridded variables 
    """

    if grid is None:
        raise ValueError("No grid was supplied")

    grid_type = None

    # find the grid type
    if isinstance(grid, pd.DataFrame):
        grid_type = "df"

    # If the grid is an xarray object, we need to convert it to .nc
    if isinstance(grid, xr.Dataset):
        grid_type = "xr"
        temp_nc = temp_file("nc") 
        nc_created.append(temp_nc)
        grid.to_netcdf(temp_nc)
        grid = temp_nc

    if type(grid) is str:
        if os.path.exists(grid) == False:
            raise ValueError("grid file supplied does not exist")
        if grid.endswith(".nc") == False:
            raise ValueError("grid file supplied is not a netcdf file!")
        grid_type = "nc"


    if "DataSet" in str(type(grid)):
        if type(grid.current) is str:
            grid = grid.current
        else:
            grid = grid.current[0]
            print("Warning: first file in tracker used for regridding!")
        grid_type = "nc"

    if grid_type is None:
        raise ValueError("grid supplied is not valid")

    # check that the remapping method is valid
    if (method in {"bil", "dis", "nn"}) == False:
        raise ValueError("remapping method is invalid. Please check")
     
     # need code at this point to add missing grid if it's needed
     
     # same with na_value stuff. But maybe that isn't really needed
     # a distraction?
     
     # check the number of grids in the file

    # Do do the horizontal regridding

    grid_split = dict()

    if type(self.current) is str:
        self.current = [self.current]
    
    if type(self.current) is list:
        for ff in self.current:
            cdo_result = os.popen( "cdo griddes " + ff).read()
            if cdo_result in grid_split:
                grid_split[cdo_result].append(ff)
            else:
                grid_split[cdo_result] = [ff]

    if grid is not None:
                   # first generate the grid
        if self.grid is None:
            if grid_type == "df":
                self.grid = generate_grid(grid)
                nc_created.append(self.grid)
            else:
                self.grid = grid
    new_files = []

    for key in grid_split:
        # first we need to generate the weights for remapping
        # and add this to the files created list and self.weights
        if self.run == False:
            raise ValueError("You cannot generate weights as part of a chain currently")
        tracker = open_data(grid_split[key])

        weights_nc = temp_file("nc") 

        nc_created.append(weights_nc)

        if type(tracker.current) is list:
            cdo_command = "cdo -gen" + method + ","+ self.grid + " " + tracker.current[0] + " " +  weights_nc
        else:
            cdo_command = "cdo -gen" + method + ","+ self.grid + " " + tracker.current + " " +  weights_nc

        os.system(cdo_command)
        if os.path.exists(weights_nc) == False:
            raise ValueError("Creation of weights failed!")

        cdo_command= "cdo -remap," + self.grid + "," + weights_nc 

        run_this(cdo_command, tracker,  output = "ensemble", cores = cores)
        if type(tracker.current) is str:
            new_files += [tracker.current]
            nc_safe.append(tracker.current)
        else:
            new_files += tracker.current
            for ff in tracker.current:
                nc_safe.append(ff)
        self.history.append(cdo_command)

    self.current = new_files 
    if len(self.current) == 1:
        self.current = self.current[0]

   # if len(grid_split) > 1:
   #     self.grid = None
   #     self.weights = None
   # else:
   #     self.weights = weights_nc 

   # keep = []
   # if self.weights is not None:
   #     keep.append(self.weights)

   # if self.grid is not None:
   #     keep.append(self.grid)

    if type(self.current) is str:
        keep.append(self.current)
    else:
        for ff in self.current:
            keep.append(ff)

    cleanup(keep = keep) 
    
