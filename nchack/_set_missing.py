
import os
import tempfile

from .flatten import str_flatten
from ._variables import variables
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def set_missing(self, value, silent = True):
    """Function to set the missing values"""
    """This is either a range or a single value"""

    if type(value) is int:
        value = float(value)

    if type(value) is float:
        cdo_command = "cdo setctomiss," + str(value)
    if type(value) is list:
        cdo_command = "cdo setrtomiss," + str(value[0]) + "," + str(value[1])

    run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

    
