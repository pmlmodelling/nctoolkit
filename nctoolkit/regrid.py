
import copy
import os
import pandas as pd
import subprocess
import warnings
import xarray as xr

from nctoolkit.api import open_data
from nctoolkit.cleanup import cleanup, disk_clean
from nctoolkit.flatten import str_flatten
from nctoolkit.generate_grid import generate_grid
from nctoolkit.runthis import run_this, run_cdo
from nctoolkit.session import nc_safe
from nctoolkit.temp_file import temp_file


def regrid(self, grid=None, method="bil"):
    """
    Regrid a dataset to a target grid

    Parameters
    -------------
    grid : nctoolkit.DataSet, pandas data frame or netcdf file
        The grid to remap to

    method : str
        Remapping method. Defaults to "bil". Methods available are: bilinear - "bil"; nearest neighbour - "nn" - "nearest neighbour"; "bic" - "bicubic interpolation";
    """

    del_grid = None
    if grid is None:
        raise ValueError("No grid was supplied")

    grid_type = None

    # find the grid type
    if isinstance(grid, pd.DataFrame):
        grid_type = "df"

    if type(grid) is str:
        if os.path.exists(grid) == False:
            raise ValueError("grid file supplied does not exist")
        grid_type = "nc"

    if "DataSet" in str(type(grid)):
        grid.run()
        if type(grid.current) is str:
            grid = grid.current
        else:
            grid = grid.current[0]
            warnings.warn(message="The first file in dataset used for regridding!")
        grid_type = "nc"

    if grid_type is None:
        raise ValueError("grid supplied is not valid")

    # check that the remapping method is valid
    if (method in {"bil", "bic", "nn"}) == False:
        raise ValueError("remapping method is invalid. Please check")

    # check the number of grids in the dataset

    # Do do the horizontal regridding

    grid_split = dict()

    self.run()

    if type(self.current) is list:
        orig_files = copy.deepcopy(self.current)
    else:
        orig_files = [copy.deepcopy(self.current)]

    for ff in self:
        cdo_result = subprocess.run(
            f"cdo griddes {ff}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
        cdo_result = str(cdo_result)
        if cdo_result in grid_split:
            grid_split[cdo_result].append(ff)
        else:
            grid_split[cdo_result] = [ff]

    if grid is not None:
        # first generate the grid
        if grid_type == "df":
            target_grid = generate_grid(grid)
            del_grid = copy.deepcopy(target_grid)
            nc_safe.append(del_grid)
        else:
            target_grid = grid
    new_files = []

    for key in grid_split:
        # first we need to generate the weights for remapping
        # and add this to the files created list and self.weights
        tracker = open_data(grid_split[key], suppress_messages=True)

        weights_nc = temp_file("nc")

        if type(tracker.current) is list:
            cdo_command = (
                f"cdo -gen{method},{target_grid} {tracker.current[0]} {weights_nc}"
            )
        else:
            cdo_command = (
                f"cdo -gen{method},{target_grid} {tracker.current} {weights_nc}"
            )

        weights_nc = run_cdo(cdo_command, target=weights_nc)

        cdo_command = f"cdo -remap,{target_grid},{weights_nc}"

        tracker._execute = True

        nc_safe.append(weights_nc)

        run_this(cdo_command, tracker, output="ensemble")

        nc_safe.remove(weights_nc)

        if type(tracker.current) is str:
            new_files += [tracker.current]
        else:
            new_files += tracker.current

        for ff in new_files:
            nc_safe.append(ff)

        self.history += tracker.history

        self._hold_history = copy.deepcopy(self.history)

    if del_grid is not None:
        if del_grid in nc_safe:
            nc_safe.remove(del_grid)

    for ff in new_files:
        if ff in nc_safe:
            nc_safe.remove(ff)

    self.current = new_files

    cleanup()
    self.disk_clean()
