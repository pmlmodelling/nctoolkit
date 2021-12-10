import copy
import os
import pandas as pd
import subprocess
import warnings

from nctoolkit.api import open_data
from nctoolkit.cleanup import cleanup
from nctoolkit.generate_grid import generate_grid
from nctoolkit.runthis import run_this, run_cdo
from nctoolkit.session import nc_safe, append_safe, remove_safe, get_safe
from nctoolkit.temp_file import temp_file


def regrid(self, grid=None, method="bil", recycle=False):
    """
    Regrid a dataset to a target grid

    Parameters
    -------------
    grid : nctoolkit.DataSet, pandas data frame or netCDF file
        The grid to remap to

    method : str
        Remapping method. Defaults to "bil". Methods available are:
        bilinear - "bil";
        nearest neighbour - "nn" - "nearest neighbour"
        bicubic interpolation - "bic"
        Distance-weighted average - "dis"
        First order conservative remapping - "con"
        Second order conservative remapping - "con2"
        Large area fraction remapping - "laf"
    """

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    valid_methods = ["bil", "nn", "bic", "dis", "con", "con2", "laf"]

    if "DataSet" in str(type(grid)):
        if grid._weights is not None and grid._grid is not None:
            target_grid = grid._grid
            weights_nc = grid._weights
            cdo_command = f"cdo -remap,{target_grid},{weights_nc}"
            run_this(cdo_command, self, output="ensemble")

            return None

    del_grid = None
    if grid is None:
        raise ValueError("No grid was supplied")

    grid_type = None

    # find the grid type
    if isinstance(grid, pd.DataFrame):
        grid_type = "df"
        if len(grid) == 0:
            raise ValueError("You have supplied an empty data frame as a grid!")

    if type(grid) is str:
        if os.path.exists(grid) is False:
            raise ValueError("grid file supplied does not exist")
        grid_type = "nc"

    if "DataSet" in str(type(grid)):
        grid.run()
        if len(grid) > 1:
            warnings.warn(message="The first file in dataset used for regridding!")
        grid = grid.current[0]
        grid_type = "nc"

    if grid_type is None:
        raise ValueError("grid supplied is not valid")

    # check that the remapping method is valid
    if (method in valid_methods) is False:
        raise ValueError("remapping method is invalid. Please check")

    # check the number of grids in the dataset

    # Do do the horizontal regridding

    grid_split = dict()

    self.run()

    if len(self) > 1 and recycle:
        raise ValueError("You cannot recycle multi-file datasets")

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
            append_safe(del_grid)
        else:
            target_grid = grid
    new_files = []

    if recycle:
        append_safe(target_grid)

    for key in grid_split:
        # first we need to generate the weights for remapping
        # and add this to the files created list and self.weights
        tracker = open_data(
            grid_split[key], suppress_messages=True, thredds=self._thredds
        )

        if tracker._precision != "default":
            tracker.set_precision(self._precision)

        weights_nc = temp_file("nc")

        cdo_command = (
            f"cdo -gen{method},{target_grid} {tracker.current[0]} {weights_nc}"
        )

        try:
            weights_nc = run_cdo(
                cdo_command, target=weights_nc, precision=self._precision
            )
        except Exception as e:
            del tracker
            remove_safe(weights_nc)
            raise ValueError(e)

        if recycle:
            self._weights = weights_nc
            self._grid = target_grid

        cdo_command = f"cdo -remap,{target_grid},{weights_nc}"

        tracker._execute = True

        run_this(cdo_command, tracker, output="ensemble")

        if recycle == False:
            remove_safe(weights_nc)

        for ff in tracker:
            append_safe(ff)

        new_files += tracker.current

        self.history += tracker.history

        self._hold_history = copy.deepcopy(self.history)

    if del_grid is not None:
        if recycle == False:
            remove_safe(del_grid)

    self.current = new_files

    for ff in self:
        if len([x for x in get_safe() if x == ff]) > 1:
            remove_safe(ff)

    self._thredds = False
    cleanup()
    self.disk_clean()
