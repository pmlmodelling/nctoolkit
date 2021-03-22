import copy
import subprocess
import warnings

from nctoolkit.api import open_data
from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this


def bottom(self):
    """
    Extract the bottom level from a dataset
    This extracts the bottom level from each netCDF file. Please note that for
    ensembles, it uses the first file to derive the index of the bottom level.
    Use bottom_mask for files when the bottom cell in netCDF files do not represent
    the actual bottom.

    Examples
    ------------

    If you wanted to extract the bottom vertical level of a dataset, do the following:

    >>> ds.bottom()

    This method is most useful for things like oceanic model data, where the bottom cell corresponds to the bottom of the ocean.

    """

    # extract the number of the bottom level
    # Use the first file for an ensemble
    # pull the cdo command together, then run it or store it
    if len(self) > 1:
        ff = self.current[0]
        warnings.warn(
            message="The first file in ensemble used to determine number of "
            "vertical levels"
        )
    else:
        ff = self.current[0]

    cdo_result = subprocess.run(
        "cdo nlevel " + ff, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout
    n_levels = int(
        str(cdo_result).replace("b'", "").strip().replace("'", "").split("\\n")[0]
    )

    cdo_command = f"cdo -sellevidx,{str(n_levels)}"

    run_this(cdo_command, self, output="ensemble")


def surface(self):
    """
    Extract the top/surface level from a dataset
    This extracts the first vertical level from each file in a dataset.

    Examples
    ------------

    If you wanted to extract the top vertical level of a dataset, do the following:

    >>> ds.surface()

    This method is most useful for things like oceanic data, where this method will extract the sea surface.
    """

    cdo_command = "cdo -sellevidx,1"
    run_this(cdo_command, self, output="ensemble")


def vertical_interp(self, levels=None):
    """
    Verticaly interpolate a dataset based on given vertical levels
    This is calculated for each time step and grid cell

    Parameters
    -------------
    levels : list, int or str
        list of vertical levels, for example depths for an ocean model, to vertically
        interpolate to. These must be floats or ints.

    Examples
    ------------

    If you wanted to vertically interpolate a dataset to 5 and 10 metres, you would do the following:

    >>> ds.vertical_interp([5,10])

    This method is most useful for things like oceanic data, where you need to interpolate to certain depth levels.
    It will require that vertical levels are the same in every grid cell.

    """

    if levels is None:
        raise ValueError("Please supply vertical depths")

    # first a quick fix for the case when there is only one vertical depth

    if (type(levels) == int) or (type(levels) == float):
        levels = {levels}

    for vv in levels:
        if (type(vv) is not float) and (type(vv) is not int):
            raise TypeError(f"{vv} is not a valid depth")

    levels = str_flatten(levels, ",")
    cdo_command = f"cdo -intlevel,{levels}"

    run_this(cdo_command, self, output="ensemble")


def vertstat(self, stat="mean"):
    """Method to calculate the vertical mean from a function"""
    cdo_command = f"cdo -vert{stat}"
    run_this(cdo_command, self, output="ensemble")


def vertical_mean(self):
    """
    Calculate the depth-averaged mean for each variable
    This is calculated for each time step and grid cell

    Examples
    ------------

    If you wanted to vertical mean of every variable in a dataset, you would do this:

    >>> ds.vertical_mean()

    This method will calculate the vertical mean weighted by the thickness of each cell. Note that
    if cell thickness cannot be derived it will just average the values in each vertical cell.


    """
    vertstat(self, stat="mean")


def vertical_min(self):
    """
    Calculate the vertical minimum of variable values
    This is calculated for each time step and grid cell

    Examples
    ------------

    If you wanted to vertical minimum of every variable in a dataset, you would do this:

    >>> ds.vertical_min()

    """
    vertstat(self, stat="min")


def vertical_max(self):
    """
    Calculate the vertical maximum of variable values
    This is calculated for each time step and grid cell

    Examples
    ------------

    If you wanted to vertical maximum of every variable in a dataset, you would do this:

    >>> ds.vertical_max()

    """
    vertstat(self, stat="max")


def vertical_range(self):
    """
    Calculate the vertical range of variable values
    This is calculated for each time step and grid cell

    Examples
    ------------

    If you wanted to range of values across all vertical levels of every variable in a dataset, you would do this:

    >>> ds.vertical_range()

    """
    vertstat(self, stat="range")


def vertical_sum(self):
    """
    Calculate the vertical sum of variable values
    This is calculated for each time step and grid cell

    Examples
    ------------

    If you wanted to sum of values across all vertical levels of every variable in a dataset, you would do this:

    >>> ds.vertical_sum()

    """
    vertstat(self, stat="sum")


def vertical_cumsum(self):
    """
    Calculate the vertical sum of variable values
    This is calculated for each time step and grid cell

    Examples
    ------------

    If you wanted to calculate the cumulative sum of values across all vertical levels of every variable in a dataset, you would do this:

    >>> ds.vertical_sum()

    The cumulative sum will be calculated from the first to the last vertical level. For example, in oceanic data it would start at the sea surface.
    """
    vertstat(self, stat="cum")


def invert_levels(self):
    """
    Invert the levels of 3D variables
    This is calculated for each time step and grid cell

    Examples
    ------------

    If you wanted to invert the vertical levels, you would do this:

    >>> ds.invert_levels()

    """
    cdo_command = "cdo -invertlev"

    run_this(cdo_command, self, output="ensemble")


def bottom_mask(self):
    """
    Create a mask identifying the deepest cell without missing values.
    This converts a dataset to a mask identifying which cell represents the bottom,
    for example the seabed. 1 identifies the deepest cell with non-missing values.
    Everything else is 0, or missing. At present this method only uses the first
    available variable from netCDF files, so it may not be suitable for all data
    """
    self.run()

    if len(self) > 1:
        raise TypeError("This only works for single file datasets")
    data = open_data(self.current)

    if len(data.variables_detailed.query("levels>1")) == 0:
        raise ValueError("There is only one vertical level in this file!")

    var_use = data.variables_detailed.query("levels>1").variable[0]
    data.select(variables=var_use)
    data.select(timesteps=0)
    data.set_missing([0, 0])
    data.cdo_command(f"expr,'Wet={var_use}=={var_use}'")
    data.invert_levels()
    data.run()
    bottom = data.copy()
    bottom.vertical_cumsum()
    bottom.compare("==1")
    bottom.multiply(data)
    bottom.invert_levels()
    bottom.rename({"Wet": "bottom"})
    bottom.set_longnames({"bottom": "Identifier for cell nearest seabed"})
    bottom.set_missing([0, 0])
    bottom.run()

    self.current = copy.deepcopy(bottom.current)

    self.history = copy.deepcopy(bottom.history)
    self._hold_history = copy.deepcopy(self.history)

    cleanup()
