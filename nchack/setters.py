# todo:
    # add checker for date validity

import copy

from .temp_file import temp_file
from .session import nc_safe
from .cleanup import cleanup
from .cleanup import disk_clean
from .runthis import run_this
from .runthis import run_nco


def set_date(self, year, month, day,  base_year = 1900):

    """
    Set the date in a dataset
    You should only do this if you have to fix/change a dataset with a single, not multiple dates.

    Parameters
    -------------
    year : int
        The year
    month : int
        The month
    day : int
        The day
    base_year : int
        The base year for time creation in the netcdf. Defaults to 1900.

    """

    # check that the values supplied are valid
    # This will convert things to ints, and if it can't be done, throw an error
    if type(year) is not int:
        year = float(year)
    if type(month) is not int:
        month = float(month)

    if type(day) is not int:
        day = float(day)
    cdo_command = "cdo -L -setreftime," + str(base_year) + "-01-01 -setdate," + str(year) + "-" + str(month) + "-" + str(day)

    run_this(cdo_command, self,  output = "ensemble")


def set_missing(self, value):
    """
    Set the missing value for a single number or a range

    Parameters
    -------------
    value : 2 variable list
        Values between the two values (inclusive) of the list are set to missing.

    """

    if type(value) is list:
        cdo_command = "cdo -setrtomiss," + str(value[0]) + "," + str(value[1])

    run_this(cdo_command, self,  output = "ensemble")


def set_units(self, var_dict):
    """
    Set the units for variables

    Parameters
    -------------
    var_dict : dict
        A dictionary where the key, value pair are the variables and new units respectively.

    """


    # Check that a dictionary has been supplied
    if type(var_dict) is not dict:
        TypeError("A dictionary has not been supplied!")

    # change the units in turn. This doesn't seem to be something you can chain?
    for i in var_dict:
        cdo_command = ""
        cdo_command = cdo_command + " -setattribute," + i + "@units=" + '"' + var_dict[i]  + '"'
        cdo_command = "cdo " + cdo_command
        run_this(cdo_command, self,  output = "ensemble")




def set_longnames(self, var_dict):
    """
    Set long name

    Parameters
    -------------
    var_dict : dict
        Dictionary with key, value pairs representing the variable names and their long names

    """

    self.release()

    if type(var_dict) is not dict:
        TypeError("A dictionary has not been supplied!")

    # change the units in turn. This doesn't seem to be something you can chain?


    if type(self.current) is list:
        ff_list = self.current
    else:
        ff_list = [self.current]

    new_commands = []
    new_files = []


    for ff in ff_list:
        nco_command = "ncatted "
        for i in var_dict:
            i_dict = var_dict[i]
            i_dict = i_dict.replace('"', "'")
            nco_command += "-a long_name," + i + ',o,c,"' + i_dict   + '" '

        target = temp_file("nc")

        nco_command+= ff + " " + target

        target = run_nco(nco_command, target)

        new_files.append(target)
        new_commands.append(nco_command)

    self.history+=new_commands
    self._hold_history = copy.deepcopy(self.history)

    for ff in ff_list:
        if ff in nc_safe:
            nc_safe.remove(ff)


    self.current = new_files

    for ff in self.current:
        nc_safe.append(ff)

    if len(self.current) == 1:
        self.current = self.current[0]

    # clean up the directory
    cleanup()
    self.disk_clean()








