import subprocess
import warnings
import copy
from nctoolkit.cleanup import cleanup
from nctoolkit.api import open_data
from nctoolkit.flatten import str_flatten
import nctoolkit.api as api


def bottom(self):
    """
    bottom: Extract the bottom level from a dataset

    This extracts the bottom level from each netCDF file. Please note that for
    ensembles, it uses the first file to derive the index of the bottom level.

    You may need to double check that the bottom vertical level is the sea 'bottom' etc., as this is not always the case.

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

    cdo_command = f"-sellevidx,{str(n_levels)}"

    self.cdo_command(cdo_command, ensemble=False)


def top(self):
    """
    top: Extract the top/surface level from a dataset

    This extracts the first vertical level from each file in a dataset.

    This method is most useful for things like oceanic data, where this method will extract the sea surface.

    You may need to double check that the first vertical level is the surface, as this is not always the case.

    Examples
    ------------

    If you wanted to extract the top vertical level of a dataset, do the following:

    >>> ds.top()

    """

    cdo_command = "-sellevidx,1"
    self.cdo_command(cdo_command, ensemble=False)


def vertical_interp(
    self, levels=None, fixed=None, thickness=None, depths=None, surface=None
):
    """
    vertical_interp: Verticaly interpolate a dataset based on given vertical levels

    Vertical interpolation is calculated for each time step and grid cell

    Note
    ------
    This requires consistent vertical levels in space. For the likes of sigma-coordinates,
    please use to_zlevels.

    Parameters
    -------------
    levels : list, int or str
        list of vertical levels, for example depths for an ocean model, to vertically
        interpolate to. These must be floats or ints.
    fixed : bool
        Define whether the vertical levels are the same in all spatial locations.
        Set to True if they are, e.g. you have z-levels. If you have the likes of sigma-coordinates,
        set this to False.
    thickness: str or Dataset
        This or depths must be supplied if fixed is False, otherwise vertical thickness/depth cannot be known.
        Option argument when vertical levels vary in space.
        One of: a variable, in the dataset, which contains the variable thicknesses; a .nc file which contains
        the thicknesses; or a Dataset that contains the thicknesses. Note: the .nc file or Dataset must only contain
        one variable. Thickness should be in metres. Vertical interpolation will take the value from the mid-point of the level.
    depths: str or Dataset
        This or thickness must be supplied if fixed is False, otherwise vertical thickness/depth cannot be known.
        Option argument when vertical levels vary in space.
        One of: a variable, in the dataset, which contains the variable depths; a .nc file which contains
        the depths; or a Dataset that contains the depths. Note: the .nc file or Dataset must only contain
        one variable. Depths should be in metres, and be the mid-point of the level.
    surface: str
        If thickness is supplied you must also supply this to identify whether the top or bottom of the level is the surface, i.e. the lowest level.
        This must be one of 'top' or 'bottom'.


    Examples
    ------------

    If you wanted to vertically interpolate a dataset with spatially consistent vertical levels to 5 and 10 metres, you would do the following:

    >>> ds.vertical_interp(levels = [5,10], fixed = True)

    This method is most useful for things like oceanic data, where you need to interpolate to certain depth levels.
    It will require that vertical levels are the same in every grid cell.

    """

    # check surface

    if surface is not None:
        if surface not in ["top", "bottom"]:
            raise ValueError("Surface must be one of 'top' or 'bottom'")

    if thickness is not None:
        if depths is not None:
            if surface is None:
                raise ValueError("Please provide surface")

    if fixed is None:
        if thickness is None:
            raise ValueError("You must provide the fixed arg")

    if depths is None:
        if fixed is False:
            if thickness is None:
                raise ValueError("Please provide thickness")

    if not isinstance(fixed, bool):
        if thickness is None:
            raise TypeError("fixed must be a bool")

    if thickness is not None:
        fixed = False

    if fixed is False:
        self.to_zlevels(
            levels=levels, thickness=thickness, depths=depths, surface=surface
        )
        return None

    if levels is None:
        raise ValueError("Please supply vertical depths")

    # first a quick fix for the case when there is only one vertical depth

    if isinstance(levels, (int, float)):
        levels = [levels]

    # levels = [float(x) for x in levels]

    for vv in levels:
        if not isinstance(vv, (int, float)):
            raise TypeError(f"{vv} is not a valid depth")

    levels = str_flatten(levels, ",")
    cdo_command = f"-intlevel,{levels}"

    self.cdo_command(cdo_command, ensemble=False)


def vertstat(self, stat="mean"):
    """Method to calculate the vertical mean from a function"""
    cdo_command = f"-vert{stat}"
    self.cdo_command(cdo_command, ensemble=False)


def vertical_mean(self, thickness=None, depth_range=None, fixed=None):
    """
    vertical_mean: Calculate the depth-averaged mean for each variable.

    This is calculated for each time step and grid cell.

    Optional parameters
    -------------
    thickness: str or Dataset
        This must be supplied when vertical levels vary in space, i.e. fixed=False.
        One of: a variable, in the dataset, which contains the variable thicknesses; a .nc file which contains
        the thicknesses; or a Dataset that contains the thicknesses. Note: the .nc file or Dataset must only contain
        one variable.
    depth_range: list
        Only use when vertical levels vary in space
        Set a depth range if desired. Should be of the form [min_depth, max_depth].
    fixed : bool
        Define whether the vertical levels are the same in all spatial locations.
        Set to True if they are, e.g. you have z-levels. If you have the likes of sigma-coordinates,
        set this to True.

    Examples
    ------------

    If you wanted to vertical mean of every variable in a dataset with consistent vertical levels, you would do this:

    >>> ds.vertical_mean(fixed = True)


    This method will calculate the vertical mean weighted by the thickness of each cell. Note that
    if cell thickness cannot be derived it will just average the values in each vertical cell.


    """

    if fixed is None and thickness is None:
        raise ValueError("Please state if levels are fixed or provide thickness")

    if fixed is False:
        if thickness is None:
            raise ValueError("Please provide thickness")

    if thickness is None and depth_range is None:
        vertstat(self, stat="mean")
        return None

    if isinstance(depth_range, list):
        if len(depth_range) != 2:
            raise ValueError("Please provide a 2 variable list for depth range")
        if depth_range[1] <= depth_range[0]:
            raise ValueError("Please provide a correctly ordered depth range")

    if depth_range is not None:
        if not isinstance(depth_range, list):
            raise TypeError("Please provide a list for the depth range!")

    if not isinstance(thickness, api.DataSet):
        if thickness is None or isinstance(thickness, str) is False:
            raise ValueError("Please provide a thickness variable")

    self.run()

    self1 = self.copy()

    if len(self) > 1:
        warnings.warn(
            "Vertical structure will be assumed to be the same for all files in the dataset"
        )

    # Set up the thickness

    sorted = False

    if isinstance(thickness, api.DataSet):
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
    if isinstance(depth_range, list):
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
        self1.drop(variables=drop_this)

    ds_thick.run()
    self1.run()
    self1.multiply(ds_thick)
    warnings.warn(
        message="Assuming missing values are in the same grid cells in thickness and variable data. Modify thickness and re-run if they are not."
    )
    self1.run()
    self1.vertical_sum()
    self1.run()

    ds_thick.vertical_sum()
    self1.divide(ds_thick)
    self1.run()

    del ds_thick
    if isinstance(depth_range, list):
        del ds_depth

    self.current = self1.current
    self.history = self1.history
    self._hold_history = self1._hold_history


def vertical_min(self):
    """
    vertical_min: Calculate the vertical minimum of variable values.

    This is calculated for each time step and grid cell.

    Examples
    ------------

    If you wanted to vertical minimum of every variable in a dataset, you would do this:

    >>> ds.vertical_min()

    """
    vertstat(self, stat="min")


def vertical_max(self):
    """
    vertical_max: Calculate the vertical maximum of variable values.

    This is calculated for each time step and grid cell.

    Examples
    ------------

    If you wanted to vertical maximum of every variable in a dataset, you would do this:

    >>> ds.vertical_max()

    """
    vertstat(self, stat="max")


def vertical_range(self):
    """
    vertical_range: Calculate the vertical range of variable values.

    This is calculated for each time step and grid cell.

    Examples
    ------------

    If you wanted to range of values across all vertical levels of every variable in a dataset, you would do this:

    >>> ds.vertical_range()

    """
    vertstat(self, stat="range")


def vertical_integration(self, thickness=None, depth_range=None, fixed=None):
    """
    vertical_integration: Calculate the vertically integrated sum over the water column.

    This calculates the sum of the variable multiplied by the cell thickness

    Parameters
    -------------
    thickness: str or Dataset
        This must be supplied when vertical levels vary spatially.
        One of: a variable, in the dataset, which contains the variable thicknesses; a .nc file which contains
        the thicknesses; or a Dataset that contains the thicknesses. Note: the .nc file or DataSet must only contain
        one variable.
    depth_range: list
        Set a depth range if desired. Should be of the form [min_depth, max_depth].
    fixed : bool
        Define whether the vertical levels are the same in all spatial locations.
        Set to True if they are, e.g. you have z-levels. If you have the likes of sigma-coordinates,
        set this to True.

    Examples
    ------------

    If you wanted to integrate values across all vertical levels of every variable in a dataset that has spatially fixed vertical levels, you would do this:

    >>> ds.vertical_integration(fixed = True)

    """
    if fixed is None and thickness is None:
        raise ValueError("Please state if levels are fixed or provide thickness")

    if fixed:
        warnings.warn("Extracting vertical thickness from dataset level data")
        var = list(self.contents.query("nlevels > 1").variable)[0]

        ff = self[0]
        command = f"cdo zaxisdes {ff}"
        out = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        result, ignore = out.communicate()

        if "bounds" not in result.decode("utf-8").lower():
            raise ValueError(
                "Vertical bounds info does not appear to be in the netCDF files, so thicknesses cannot be calculated for vertical integration!"
            )

        thickness = self.copy()
        thickness.subset(time=0, variable=var)
        thickness.rename({var: "thickness"})
        thickness.assign( thickness=lambda x: (isnan(x.thickness) is False) * level(x.thickness), drop=True,)
        thickness.assign( thickness=lambda x: thickness(x.thickness) + (x.thickness < x.thickness), drop=True,)
        thickness.run()

    if thickness is None:
        raise ValueError("Please specify thickness")

    if isinstance(depth_range, list):
        if len(depth_range) != 2:
            raise ValueError("Please provide a 2 variable list for depth range")
        if depth_range[1] <= depth_range[0]:
            raise ValueError("Please provide a correctly ordered depth range")

    drop_this = None
    if depth_range is not None:
        if not isinstance(depth_range, list):
            raise TypeError("Please provide a list for the depth range!")

    if not isinstance(thickness, api.DataSet):
        if thickness is None or isinstance(thickness, str) is False:
            raise ValueError("Please provide a thickness variable")

    self.run()

    if len(self) > 1:
        warnings.warn(
            "Vertical integration will assume all files have the same structure"
        )

    # Set up the thickness

    self1 = self.copy()

    sorted = False

    if isinstance(thickness, api.DataSet):
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
    if isinstance(depth_range, list):
        if thick_var != "thickness":
            ds_thick.rename({thick_var: "thickness"})
            ds_thick.run()
        ds_depth = ds_thick.copy()
        ds_depth.vertical_cumsum()
        ds_depth.rename({"thickness": "depths"})
        ds_thick.append(ds_depth)
        ds_thick.merge()

        ds_thick.assign(z_min=lambda x: x.depths - x.thickness)
        ds_thick.assign( z_min=lambda x: x.z_min * (x.z_min >= depth_range[0]) + depth_range[0] * (x.z_min < depth_range[0]))
        ds_thick.assign( depths=lambda x: x.depths * (x.depths <= depth_range[1]) + depth_range[1] * (x.depths > depth_range[1]))
        ds_thick.assign(thickness=lambda x: x.depths - x.z_min, drop=True)
        ds_thick.assign(thickness=lambda x: x.thickness * (x.thickness > 0), drop=True)

    self1.subset(variables=self1.contents.query("nlevels > 1").variable)
    if drop_this is not None:
        self1.drop(variables=drop_this)

    ds_thick.run()
    self1.run()
    self1.multiply(ds_thick)
    self1.run()
    self1.vertical_sum()
    self1.run()
    del ds_thick
    if isinstance(depth_range, list):
        del ds_depth

    self.current = self1.current
    self.history = self1.history
    self._hold_history = self1._hold_history


def vertical_sum(self):
    """
    vertical_sum: Calculate the vertical sum of variable values.

    This is calculated for each time step and grid cell.

    Examples
    ------------

    If you wanted to sum of values across all vertical levels of every variable in a dataset, you would do this:

    >>> ds.vertical_sum()

    """
    vertstat(self, stat="sum")


def vertical_cumsum(self):
    """
    vertical_cumsum: Calculate the vertical sum of variable values.

    This is calculated for each time step and grid cell.

    Examples
    ------------

    If you wanted to calculate the cumulative sum of values across all vertical levels of every variable in a dataset, you would do this:

    >>> ds.vertical_sum()

    The cumulative sum will be calculated from the first to the last vertical level. For example, in oceanic data it would start at the sea surface.
    """
    vertstat(self, stat="cum")


def bottom_mask(self):
    """
    bottom_mask: Create a mask identifying the deepest cell without missing values..

    This converts a dataset to a mask identifying which cell represents the bottom,
    for example the seabed. 1 identifies the deepest cell with non-missing values.
    Everything else is 0, or missing.

    Note
    ------
    This will only work for single file datasets.
    The method will modify the dataset in place, so make a copy if you want to keep the original.

    Examples
    ------------

    If you wanted to create a mask identifying the bottom, you would do this:

    >>> ds.bottom_mask()
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
    data.cdo_command(f"-expr,'Wet={var_use}=={var_use}'")
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
    surface_mask: Create a mask identifying the shallowest cell without missing values.

    This converts a dataset to a mask identifying which cell represents top level,
    for example the sea surface. 1 identifies the shallowest cell with non-missing values.
    Everything else is 0, or missing. At present this method only uses the first
    available variable from netCDF files, so it may not be suitable for all data

    Examples
    ------------

    If you wanted to create a mask identifying the surface, you would do this:

    >>> ds.surface_mask()
    """

    self.invert_levels()
    self.bottom_mask()
    self.invert_levels()
