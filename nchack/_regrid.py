import os
import tempfile

from ._generate_grid import generate_grid
from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runthis import run_this

def regrid(self, grid = None, method = "bil", silent = True, cores = 1):
    """Method to regrid a netcdf file"""

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
            if self.run == False:
                raise ValueError("You cannot generate weights as part of a chain currently")
            weights_nc = tempfile.NamedTemporaryFile().name + ".nc"
            nc_created.append(weights_nc)
            self.weights = weights_nc
            
            weights_nc = self.weights

            cdo_command = "cdo gen" + method + ","+ self.grid 
            run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
        else:
            weights_nc = self.weights

        cdo_command= "cdo remap," + self.grid + "," + weights_nc 
        run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    cleanup(keep = [self.current, self.weights, self.grid])

    return(self)

