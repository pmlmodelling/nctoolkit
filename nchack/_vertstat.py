
import os
import tempfile

from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def vertstat(self, stat = "mean", silent = True):
    """Function to calculate the vertical mean from a function""" 
    cdo_command = "cdo --reduce_dim -vert" + stat

    run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def vertical_mean(self, silent = True):
    return vertstat(self, stat = "mean", silent = True)

def vertical_min(self, silent = True):
    return vertstat(self, stat = "min", silent = True)

def vertical_max(self, silent = True):
    return vertstat(self, stat = "max", silent = True)
    
def vertical_range(self, silent = True):
    return vertstat(self, stat = "range", silent = True)
