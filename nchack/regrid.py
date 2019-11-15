import subprocess
import warnings
import copy
import xarray as xr
import pandas as pd
import os

from .temp_file import temp_file
from .api import open_data

from .generate_grid import generate_grid
from .flatten import str_flatten
from .session import nc_safe
from .runthis import run_this
from .runthis import run_cdo

def regrid(self, grid = None, method = "bil"):

    """
    Regrid a dataset for a target grid and remapping method

    Parameters
    -------------
    grid : nchack.DataSet, xarray object, pandas data frame or netcdf file
        grid to remap to
    method : str
        remapping method. Defaults to "bil". Bilinear: "bil"; Nearest neighbour: "nn",....

    """
    lazy_eval = self.run == False

    if len(self.history) > len(self._hold_history):
        self.release()

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
            warnings.warn(message = "The first file in dataset used for regridding!")
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
            cdo_result = subprocess.run("cdo griddes " + ff, shell = True, capture_output = True)
            cdo_result = str(cdo_result.stdout)
            if cdo_result in grid_split:
                grid_split[cdo_result].append(ff)
            else:
                grid_split[cdo_result] = [ff]

    if grid is not None:
                   # first generate the grid
        if self.grid is None:
            if grid_type == "df":
                self.grid = generate_grid(grid)
            else:
                self.grid = grid
    new_files = []

    for key in grid_split:
        # first we need to generate the weights for remapping
        # and add this to the files created list and self.weights
        tracker = open_data(grid_split[key])

        weights_nc = temp_file("nc")


        if type(tracker.current) is list:
            cdo_command = "cdo -gen" + method + ","+ self.grid + " " + tracker.current[0] + " " +  weights_nc
        else:
            cdo_command = "cdo -gen" + method + ","+ self.grid + " " + tracker.current + " " +  weights_nc

        weights_nc = run_cdo(cdo_command, target = weights_nc)
        if os.path.exists(weights_nc) == False:
            raise ValueError("Creation of weights failed!")

        cdo_command= "cdo -remap," + self.grid + "," + weights_nc

        tracker.run = True
        nc_safe.append(weights_nc)
        run_this(cdo_command, tracker,  output = "ensemble")
        #nc_safe.remove(weights_nc)

        self.run = lazy_eval == False

        if type(tracker.current) is str:
            new_files += [tracker.current]
            nc_safe.append(tracker.current)
        else:
            new_files += tracker.current
            for ff in tracker.current:
                nc_safe.append(ff)
        if type(tracker.history) is list:
            self.history+=tracker.history
        else:
            self.history.append(tracker.history)

        self._hold_history = copy.deepcopy(self.history)

    self.current = new_files
    if len(self.current) == 1:
        self.current = self.current[0]




