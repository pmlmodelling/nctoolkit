import os
import tempfile

from ._generate_grid import generate_grid
from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runthis import run_this

def rename(self, newnames, silent = True, cores = 1):
    """Function to rename netcdf variable"""

    if type(newnames) is not dict:
        raise ValueError("a dictionary was not supplied")

    # now, we need to loop through the renaming dictionary to get the cdo sub
    cdo_rename = ""
    
    for key, value in newnames.items():
        cdo_rename +=  "," + key
        cdo_rename += "," + value

    # need a check at this point for file validity     
    cdo_command= "cdo chname" + cdo_rename 

    self.history.append(cdo_command)
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    cleanup(keep = self.current)

    return(self)

