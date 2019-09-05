
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def set_unit(self, unit, silent = True):
    """Function to set the date"""

    # Check that the unit supplied is a string
    if type(unit) is not str:
        ValueError("Unit supplied is not a string")

    cdo_command = "cdo -setunit,'" + unit +"'"

    run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

    
