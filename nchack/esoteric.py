# todo:
    # add checker for date validity

import copy
import os
import re

from .temp_file import temp_file
from .session import nc_safe
from .cleanup import cleanup
from .runthis import run_this
from .runthis import run_nco

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

    if grid not in ["curvilinear", "unstructured", "dereference", "regular", "regularnn", "lonlat"]:
            raise ValueError("Grid type supplies is not supported")

    cdo_command = "cdo -setgridtype," + grid

    run_this(cdo_command, self,  output = "ensemble")




def assign_coords(self, lon_name = None, lat_name = None):
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

    self.release()

    if type(lon_name) is not str:
        TypeError("Method does not yet work with ensembles")

    if type(lat_name) is not str:
        TypeError("Method does not yet work with ensembles")

    # change the units in turn. This doesn't seem to be something you can chain?

    variables = self.variables

    nco_command = "ncatted "

    for vv in variables:
        nco_command += "-a coordinates,"+ vv + ",c,c,'" + lon_name + " " + lat_name + "' "

    target = ""
    if type(self.start) is list:
        target = ""
    else:
        if self.start == self.current:
            target = temp_file("nc")

    nco_command+= self.current + " " + target

    print(nco_command)
    return None

    target = run_nco(nco_command, target)

    if target != "":
        nc_safe.remove(self.current)
        self.current = target
        nc_safe.append(self.current)

    # clean up the directory
    cleanup(keep = self.current)

    self.history.append(nco_command)
    self._hold_history = copy.deepcopy(self.history)





