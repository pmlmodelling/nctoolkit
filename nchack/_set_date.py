
import os
import tempfile

from .flatten import str_flatten
from ._depths import nc_depths 
from ._variables import variables
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runcommand import run_command

def set_date(self, year, month, day, base_year = 1900, silent = True):
    """Function to set the missing values"""
    """This is either a range or a single value"""

    ff = self.current

    target = tempfile.NamedTemporaryFile().name + ".nc"
    owd = os.getcwd()
   # log the full path of the file
    global nc_created
    nc_created.append(target)
    # check that the values supplied are valid
    # This will convert things to ints, and if it can't be done, throw an error
    if type(year) is not int:
        year = float(year)
    if type(month) is not int:
        month = float(month)

    if type(day) is not int:
        day = float(day)
    cdo_command = "cdo -setreftime," + str(base_year) + "-01-01 -setdate," + str(year) + "-" + str(month) + "-" + str(day) + " " + self.current + " " + target

    self.history.append(cdo_command)
    run_command(cdo_command, self, silent) 
    if self.run: self.current = target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

    
