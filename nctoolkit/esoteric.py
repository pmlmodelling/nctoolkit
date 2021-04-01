import copy

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
