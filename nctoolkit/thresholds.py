import copy
import os
import subprocess

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_cdo, tidy_command
from nctoolkit.session import nc_safe, session_info, append_safe, remove_safe
from nctoolkit.show import nc_variables
from nctoolkit.temp_file import temp_file
from nctoolkit.utils import cdo_version


def first_above(self, x=None):
    """
    Identify the time step when a value is first above a threshold
    This will do the comparison with either a number, a Dataset or a NetCDF file.
    Parameters
    ------------
    x: int, float, DataSet or netcdf file
        An int, float, single file dataset or netcdf file to use for the threshold(s).
        If comparing with a dataset or single file there must only be a single variable
        in it. The grids must be the same.

    Examples
    ------------

    If you wanted to calculate the first time step where the value in a grid cell goes above 10, you would do the following

    >>> data.first_above(10)


    If you wanted to calculate the first time step where the value in a grid cell goes above that in another dataset, the
    following will work. Note that both datasets must have the same grid, and can only have single variables. The second
    dataset can, of course, only have one timestep.

    >>> data.first_above(data1)


    """

    self.run()

    if len(self.variables) > 1:
        raise ValueError("This method only works with single variable datasets!")

    # 1: int, float multiplication
    if isinstance(x, (int, float)):
        self.compare(f">{x}")
        self.rename({self.variables[0]: "target"})
        self.set_missing(0)
        self.assign(new=lambda x: (x.target == x.target) * (timestep(x.target) + 1), drop=True)
        self.set_missing([0, 0.01])
        self.tmin()
        self.assign(first=lambda x: int(x.new) - 1, drop=True)
        self.run()
        return None

    # 2: dataset or netcdf file multiplication
    # get the netcdf file(s)
    if ("api.DataSet" in str(type(x))) or (type(x) is str):
        x.run()
        self.gt(x)
        self.rename({self.variables[0]: "target"})
        self.set_missing(0)
        self.assign(new=lambda x: (x.target == x.target) * (timestep(x.target) + 1), drop=True)
        self.set_missing([0, 0.01])
        self.tmin()
        self.assign(first=lambda x: int(x.new) - 1, drop=True)
        self.run()
        return None

    raise TypeError("You have not supplied a valid type for x!")
