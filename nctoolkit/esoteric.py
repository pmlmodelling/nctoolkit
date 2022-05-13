import copy
import pandas as pd
import numpy as np

from .temp_file import temp_file
from .cleanup import cleanup
from .runthis import run_this
from .runthis import run_nco
from .api import open_data

def fix_nemo_ersem_grid(self):
    """
    A quick hack to change the grid file in North West European shelf Nemo grids.

    """

    ds = open_data(self[0])

    lon_name = [x for x in ds.to_xarray().coords if "lon" in x][0]
    lat_name = [x for x in ds.to_xarray().coords if "lat" in x][0]
    lons = ds.to_xarray()[lon_name].values.flatten()
    if len(set(list(pd.DataFrame({"lon":lons}).groupby("lon").size().sort_values()))) == 1:
        raise ValueError("There appears to be nothing to fix!")
    lons =  list(set(lons))
    
    for i in range(1, len(lons)):
        if np.round(lons[i] - lons[i-1], 5) == np.round(lons[i+1] - lons[i], 5):
            break
    xinc = np.round(lons[i] - lons[i-1], 5)
    
    lats = ds.to_xarray()[lat_name].values.flatten()
    lats =  list(set(lats))
    
    for i in range(1, len(lats)):
        if np.round(lats[i] - lats[i-1], 5) == np.round(lats[i+1] - lats[i], 5):
            break
    yinc = np.round(lats[i] - lats[i-1], 5)
    grid_file = temp_file().replace(".", "")
    ysize = ds.to_xarray()[lon_name].shape[0]
    xsize = ds.to_xarray()[lat_name].shape[1]
    xfirst = min(lons)
    lats = ds.to_xarray()[lat_name].values.flatten()
    yfirst = min(pd.DataFrame({"lat":lats}).groupby("lat").size().sort_values().reset_index()["lat"][0:-1])
    with open(grid_file, 'a') as file:
        file.write('#\n')
        file.write('# gridID 1\n')
        file.write('#\n')
        file.write('gridtype = lonlat\n')
        file.write(f'gridsize = {xsize*ysize}\n')
        file.write(f'xsize = {xsize}\n')
        file.write(f'ysize = {ysize}\n')
        file.write('xname = lon\n')
        file.write('xlongname= longitude\n')
        file.write('xunits= degrees_east\n')
        file.write('yname = lat\n')
        file.write('ylongname= latitude\n')
        file.write('yunits= degrees_north\n')
        file.write(f'xfirst= {xfirst}\n')
        file.write(f'xinc= {xinc}\n')
        file.write(f'yfirst= {yfirst}\n')
        file.write(f'yinc= {yinc}\n')
    self.cdo_command(f"setgrid,{grid_file}")
    self.run()


def no_leaps(self):
    """
    Remove leap years.
    This uses an undocumented CDO feature to remove Feb 29 and sets the calendar to leap year free

    """

    cdo_command = f"cdo -delfeb29"

    run_this(cdo_command, self, output="ensemble")


def set_gridtype(self, grid):
    """
    Set the grid type. Only use this if, for example, the grid is "generic" when it should be lonlat.

    Parameters
    -------------
    grid : str
        Grid type. Needs to be one of "curvilinear", "unstructured", "dereference", "regular", "regularnn" or "lonlat".

    """

    # check that the values supplied are valid
    # This will convert things to ints, and if it can't be done, throw an error

    if grid not in [
        "curvilinear",
        "unstructured",
        "dereference",
        "regular",
        "regularnn",
        "lonlat",
    ]:
        raise ValueError("Grid type supplies is not supported")

    cdo_command = f"cdo -setgridtype,{grid}"

    run_this(cdo_command, self, output="ensemble")


def assign_coords(self, lon_name=None, lat_name=None):
    """
    Assign coordinates to variables

    Parameters
    -------------
    lon_name : str
        Name of the longitude dimension
    lat_name : str
        Name of the latitude dimension
    """

    # add grid number check

    self.run()

    if len(self) > 1:
        raise TypeError("This only works for single files currently")

    if (lon_name is None) or (lat_name is None):
        TypeError("Please provide lon and lat names!")

    if type(lon_name) is not str:
        TypeError("Method does not yet work with ensembles")

    if type(lat_name) is not str:
        TypeError("Method does not yet work with ensembles")

    # change the units in turn. This doesn't seem to be something you can chain?

    nco_command = "ncatted "

    for vv in self.variables:
        nco_command += (
            "-a coordinates," + vv + ",c,c,'" + lon_name + " " + lat_name + "' "
        )

    target = temp_file("nc")

    nco_command += self[0] + " " + target

    target = run_nco(nco_command, target)

    self.current = target

    # clean up the directory
    cleanup()

    self.history.append(nco_command)
    self._hold_history = copy.deepcopy(self.history)


def set_attributes(self, att_dict):
    """
    Set Global attributes

    Parameters
    -------------
    att_dict : dict
        Dictionary with key, value pairs representing the attribute names and their long names

    """

    self.run()

    if type(self.current) is not str:
        TypeError("Method does not yet work with ensembles")

    if type(att_dict) is not dict:
        TypeError("A dictionary has not been supplied!")

    # change the units in turn. This doesn't seem to be something you can chain?

    nco_command = "ncatted -O -h "
    for i in att_dict:
        nco_command += "-a " + i + ",global,o,c,'" + att_dict[i] + "' "

    target = ""
    if type(self.start) is list:
        target = ""
    else:
        if self.start == self.current:
            target = temp_file("nc")

    nco_command += self.current + " " + target

    target = run_nco(nco_command, target)

    if target != "":
        self.current = target

    # clean up the directory
    cleanup(keep=self.current)

    self.history.append(nco_command)
    self._hold_history = copy.deepcopy(self.history)


def delete_attributes(self, atts):
    """
    Set Global attributes
    Parameters
    -------------
    atts : list or str
        list or str of global attributes to remove.
    """

    self.run()

    if type(self.current) is not str:
        TypeError("Method does not yet work with ensembles")

    if type(atts) not in [str, list]:
        TypeError("A dictionary has not been supplied!")

    # change the units in turn. This doesn't seem to be something you can chain?

    nco_command = "ncatted "

    if type(atts) is str:
        atts = [atts]

    for i in atts:
        i_dict = i
        nco_command += "-a " + i + ",global,d,, "

    target = ""
    if type(self.start) is list:
        target = ""
    else:
        if self.start == self.current:
            target = temp_file("nc")

    nco_command += self.current + " " + target

    target = run_nco(nco_command, target)

    if target != "":
        self.current = target

    # clean up the directory
    cleanup(keep=self.current)

    self.history.append(nco_command)
