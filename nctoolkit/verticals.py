import copy
import subprocess
import warnings
import os

from nctoolkit.api import open_data
from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this, run_cdo
from nctoolkit.temp_file import temp_file
from nctoolkit.session import append_safe
from nctoolkit.session import remove_safe

def to_zlevels(self, levels = None, thickness = None, depths = None):
    """
    Convert datasets with non z-level verticals to z-levels 
    Parameters
    -------------
    levels: list
        List of new z-levels. Must be positive and in metres.
    thickness: str or Dataset
        One of: a variable, in the dataset, which contains the variable thicknesses; a .nc file which contains
        the thicknesses; or a Dataset that contains the thicknesses. Note: the .nc file or Dataset must only contain
        one variable. Thickness should be in metres. Vertical interpolation will take the value from the mid-point of the level.
    depths: str or Dataset
        One of: a variable, in the dataset, which contains the depths of each cell; a .nc file which contains
        the depths; or a Dataset that contains the depths. Note: the .nc file or Dataset must only contain
        one variable.
    """
    self.run()

    if len(self) > 1:
        raise ValueError("This currently only works on single file datasets")

    if thickness is None and depths is None:
        if "e3t" in self.variables:
            thickness = "e3t"

    drop_this = None

    if depths is None:
        if "api.DataSet" not in str(type(thickness)):
            if thickness is None or type(thickness) is not str:
                raise ValueError("Please provide a valid thickness or depths variable")

    if thickness is None:
        if "api.DataSet" not in str(type(depths)):
            if depths is None or type(depths) is not str:
                raise ValueError("Please provide a valid thickness or depths variable")

    # Set up the thickness

    self1 = self.copy()
    ds = self.copy()

    ds.subset(variables=ds.contents.query("nlevels > 1").variable)
    ds.run()
    vars = ds.variables

    sorted = False

    if depths is None:

        if "api.DataSet" in str(type(thickness)):
            ds_depths = thickness.copy()
            ds_depths.run()
            if len(ds_depths.variables) != 1:
                raise ValueError("Please provide a thickness dataset with 1 variable!")
            sorted = True

        if sorted is False:
            if thickness in self.variables:
                ds_depths = open_data(self1[0])
                ds_depths.subset(variable=thickness)
                ds_depths.run()
                drop_this = thickness
            else:
                ds_depths = open_data(thickness)
                if len(ds_depths.variables) != 1:
                    raise ValueError("Please provide a thickness file with 1 variable!")

        thick_var = ds_depths.variables[0]

        ds_depths.rename({thick_var: "thickness"})
        ds_depths.run()
        ds_depths.vertical_cumsum()
        ds_depths.rename({"thickness": "depth"})
        ds_depths.subset(times = 0)
        ds_depths.cdo_command("setmisstoc,-9999999")
        ds_depths.run()

    if depths is not None:
        if "api.DataSet" in str(type(depths)):
            ds_depths = depths.copy()
            ds_depths.cdo_command("setmisstoc,-9999999")
            ds_depths.run()
            if len(ds_depths.variables) != 1:
                raise ValueError("Please provide a depths dataset with 1 variable!")
            sorted = True

        if sorted is False:
            if thickness in self.variables:
                ds_depths = open_data(self1[0])
                ds_depths.subset(variable=thickness)
                ds_depths.cdo_command("setmisstoc,-9999999")
                ds_depths.run()
                drop_this = thickness
            else:
                ds_depths = open_data(depths)
                ds_depths.cdo_command("setmisstoc,-9999999")
                ds_depths.run()
                if len(ds_depths.variables) != 1:
                    raise ValueError("Please provide a thickness file with 1 variable!")


    zaxis = temp_file().replace(".", "")
    append_safe(zaxis)


    line3 = "levels = " + " ".join([str(x) for x in levels]) + " \n"
    with open(zaxis, 'a') as the_file:
        x = the_file.write('zaxistype = depth_below_sea \n')
        x = the_file.write(f'size = {len(levels)} \n')
        x = the_file.write(line3)


    target = ds_depths.copy()
    target.assign(depth = lambda x: level(x.depth) + 0 * (x.depth == x.depth), drop = True)
    target.rename({"depth_2":"depth"})
    target.vertical_interp(levels = levels)
    target.run()

    out = temp_file(".nc")
    append_safe(out)

    command = f"cdo intlevel3d,{target[0]} {ds[0]}  {ds_depths[0]} {out}"

    run_cdo(command, target = out, precision = self._precision)

    test = open_data(out)
    test.cdo_command(f"setzaxis,{zaxis}")
    test.subset(variables = vars)
    test.run()
    self.current = test.current

    remove_safe(out)
    remove_safe(zaxis)





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


def top(self):
    """
    Extract the top/surface level from a dataset
    This extracts the first vertical level from each file in a dataset.

    Examples
    ------------

    If you wanted to extract the top vertical level of a dataset, do the following:

    >>> ds.top()

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


def vertical_mean(self, thickness=None, depth_range=None):
    """
    Calculate the depth-averaged mean for each variable
    This is calculated for each time step and grid cell

    Optional parameters
    -------------
    thickness: str or Dataset
        Only use when vertical levels vary in space
        One of: a variable, in the dataset, which contains the variable thicknesses; a .nc file which contains
        the thicknesses; or a Dataset that contains the thicknesses. Note: the .nc file or Dataset must only contain
        one variable.
    depth_range: list
        Only use when vertical levels vary in space
        Set a depth range if desired. Should be of the form [min_depth, max_depth].

    Examples
    ------------

    If you wanted to vertical mean of every variable in a dataset, you would do this:

    >>> ds.vertical_mean()


    This method will calculate the vertical mean weighted by the thickness of each cell. Note that
    if cell thickness cannot be derived it will just average the values in each vertical cell.


    """
    if thickness is None and depth_range is None:
        vertstat(self, stat="mean")
        return None

    if type(depth_range) is list:

        if len(depth_range) != 2:
            raise ValueError("Please provide a 2 variable list for depth range")
        if depth_range[1] <= depth_range[0]:
            raise ValueError("Please provide a correctly ordered depth range")

    if depth_range is not None:
        if type(depth_range) is not list:
            raise TypeError("Please provide a list for the depth range!")

    if "api.DataSet" not in str(type(thickness)):
        if thickness is None or type(thickness) is not str:
            raise ValueError("Please provide a thickness variable")

    self.run()

    self1 = self.copy()

    if len(self) > 1:
        warnings.warn("Vertical structure will be assumed to be the same for all files in the dataset")

    # Set up the thickness

    sorted = False

    if "api.DataSet" in str(type(thickness)):
        ds_thick = thickness.copy()
        if len(ds_thick.variables) != 1:
            raise ValueError("Please provide a thickness dataset with 1 variable!")
        sorted = True

    drop_this = None
    if sorted is False:
        if thickness in self.variables:
            ds_thick = open_data(self[0]) 
            ds_thick.subset(variable=thickness)
            ds_thick.run()
            drop_this = thickness
        else:
            ds_thick = open_data(thickness)
            if len(ds_thick.variables) != 1:
                raise ValueError("Please provide a thickness file with 1 variable!")

    thick_var = ds_thick.variables[0]
    # modify the depth if it is a list
    if type(depth_range) is list:

        ds_thick.rename({thick_var: "thickness"})
        ds_thick.run()
        ds_depth = ds_thick.copy()
        ds_depth.vertical_cumsum()
        ds_depth.rename({"thickness": "depth"})
        ds_thick.append(ds_depth)
        ds_thick.merge()
        ds_thick.assign(z_min=lambda x: x.depth - x.thickness)
        ds_thick.assign( z_min=lambda x: x.z_min * (x.z_min >= depth_range[0]) + depth_range[0] * (x.z_min < depth_range[0]))
        ds_thick.assign( depth=lambda x: x.depth * (x.depth <= depth_range[1]) + depth_range[1] * (x.depth > depth_range[1]))
        ds_thick.assign(thickness=lambda x: x.depth - x.z_min, drop=True)
        ds_thick.assign(thickness=lambda x: x.thickness * (x.thickness > 0), drop=True)

    self1.subset(variables=self.contents.query("nlevels > 1").variable)
    if drop_this is not None:
        self1.drop(variables = drop_this)

    self1.multiply(ds_thick)
    self1.vertical_sum()
    self1.run()

    ds_thick.vertical_sum()
    self1.divide(ds_thick)
    self1.run()

    del ds_thick
    if type(depth_range) is list:
        del ds_depth


    self.current = self1.current
    self.history = self1.history
    self._hold_history = self1._hold_history


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


def vertical_integration(self, thickness=None, depth_range=None):
    """
    Calculate the vertically integrated sum over the water column
    This calculates the sum of the variable multiplied by the cell thickness

    Parameters
    -------------
    thickness: str or Dataset
        One of: a variable, in the dataset, which contains the variable thicknesses; a .nc file which contains
        the thicknesses; or a Dataset that contains the thicknesses. Note: the .nc file or Dataset must only contain
        one variable.
    depth_range: list
        Set a depth range if desired. Should be of the form [min_depth, max_depth].

    Examples
    ------------

    If you wanted to sum of values across all vertical levels of every variable in a dataset, you would do this:

    >>> ds.vertical_sum()

    """

    if type(depth_range) is list:

        if len(depth_range) != 2:
            raise ValueError("Please provide a 2 variable list for depth range")
        if depth_range[1] <= depth_range[0]:
            raise ValueError("Please provide a correctly ordered depth range")

    drop_this = None
    if depth_range is not None:
        if type(depth_range) is not list:
            raise TypeError("Please provide a list for the depth range!")

    if "api.DataSet" not in str(type(thickness)):
        if thickness is None or type(thickness) is not str:
            raise ValueError("Please provide a thickness variable")

    self.run()

    if len(self) > 1:
        warnings.warn("Vertical integration will assume all files have the same structure")

    # Set up the thickness

    self1 = self.copy()

    sorted = False

    if "api.DataSet" in str(type(thickness)):
        ds_thick = thickness.copy()
        if len(ds_thick.variables) != 1:
            raise ValueError("Please provide a thickness dataset with 1 variable!")
        sorted = True

    if sorted is False:
        if thickness in self.variables:
            ds_thick = open_data(self1[0])
            ds_thick.subset(variable=thickness)
            ds_thick.run()
            drop_this = thickness
        else:
            ds_thick = open_data(thickness)
            if len(ds_thick.variables) != 1:
                raise ValueError("Please provide a thickness file with 1 variable!")

    thick_var = ds_thick.variables[0]
    # modify the depth if it is a list
    if type(depth_range) is list:

        ds_thick.rename({thick_var: "thickness"})
        ds_thick.run()
        ds_depth = ds_thick.copy()
        ds_depth.vertical_cumsum()
        ds_depth.rename({"thickness": "depth"})
        ds_thick.append(ds_depth)
        ds_thick.merge()
        ds_thick.assign(z_min=lambda x: x.depth - x.thickness)
        ds_thick.assign( z_min=lambda x: x.z_min * (x.z_min >= depth_range[0]) + depth_range[0] * (x.z_min < depth_range[0]))
        ds_thick.assign( depth=lambda x: x.depth * (x.depth <= depth_range[1]) + depth_range[1] * (x.depth > depth_range[1]))
        ds_thick.assign(thickness=lambda x: x.depth - x.z_min, drop=True)
        ds_thick.assign(thickness=lambda x: x.thickness * (x.thickness > 0), drop=True)

    self1.subset(variables=self1.contents.query("nlevels > 1").variable)
    if drop_this is not None:
        self1.drop(variables = drop_this)

    self1.multiply(ds_thick)
    self1.vertical_sum()
    self1.run()
    del ds_thick
    if type(depth_range) is list:
        del ds_depth

    self.current = self1.current
    self.history = self1.history
    self._hold_history = self1._hold_history


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

    if len(data.contents.query("nlevels>1")) == 0:
        raise ValueError("There is only one vertical level in this file!")

    var_use = data.contents.query("nlevels>1").variable[0]
    data.subset(variables=var_use)
    data.subset(timesteps=0)
    data.as_missing([0, 0])
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
    bottom.as_missing([0, 0])
    bottom.run()

    self.current = copy.deepcopy(bottom.current)

    self.history = copy.deepcopy(bottom.history)
    self._hold_history = copy.deepcopy(self.history)

    cleanup()

def surface_mask(self):
    """
    Create a mask identifying the shallowest cell without missing values.
    This converts a dataset to a mask identifying which cell represents top level,
    for example the sea surface. 1 identifies the shallowest cell with non-missing values.
    Everything else is 0, or missing. At present this method only uses the first
    available variable from netCDF files, so it may not be suitable for all data
    """

    self.invert_levels()
    self.bottom_mask()
    self.invert_levels()







