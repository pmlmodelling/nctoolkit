# todo:
    # add checker for date validity

import os

from ._temp_file import temp_file
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this


def set_date(self, year, month, day, base_year = 1900, silent = True):
    """Function to set the date"""

    # check that the values supplied are valid
    # This will convert things to ints, and if it can't be done, throw an error
    if type(year) is not int:
        year = float(year)
    if type(month) is not int:
        month = float(month)

    if type(day) is not int:
        day = float(day)
    cdo_command = "cdo -setreftime," + str(base_year) + "-01-01 -setdate," + str(year) + "-" + str(month) + "-" + str(day)

    run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)


def set_longname(self, var_dict, silent = True):
    """Method to set long names"""
    if self.run == False:
        ValueError("NCO methods do not work in hold mode")

    if type(self.current) is not str:
        ValueError("Method does not yet work with ensembles")

    if type(var_dict) is not dict:
        ValueError("A dictionary has not been supplied!")
    
    # change the units in turn. This doesn't seem to be something you can chain?
    for i in var_dict:
        target = temp_file("nc") 
        nc_created.append(target)
        var = i
        new_long = var_dict[i]
        nco_command = "ncatted -a long_name," + var + ",o,c,'" + new_long + "' " + self.current + " " + target
        self.history.append(nco_command)
        os.system(nco_command)

        if os.path.exists(target) == False:
            raise ValueError(nco_command + " was not successful. Check output")
        self.current = target

    # clean up the directory
    cleanup(keep = self.current)


def set_missing(self, value, silent = True, cores = 1):
    """Function to set the missing values"""
    """This is either a range or a single value"""

    if type(value) is int:
        value = float(value)

    if type(value) is float:
        cdo_command = "cdo -setctomiss," + str(value)
    if type(value) is list:
        cdo_command = "cdo -setrtomiss," + str(value[0]) + "," + str(value[1])

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)


def set_unit(self, var_dict, silent = True):
    """Method to set units"""

    # Check that a dictionary has been supplied
    if type(var_dict) is not dict:
        ValueError("A dictionary has not been supplied!")
    
    # change the units in turn. This doesn't seem to be something you can chain?
    for i in var_dict:
        cdo_command = ""
        cdo_command = cdo_command + " -setattribute," + i + "@units=" + '"' + var_dict[i]  + '"'
        cdo_command = "cdo " + cdo_command 
        run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)

