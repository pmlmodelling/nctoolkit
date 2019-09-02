
import os
import tempfile

from .flatten import str_flatten
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

    return(self)
    

    
