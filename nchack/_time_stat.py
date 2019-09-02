
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def time_stat(self, stat = "mean", silent = True):
    """Function to calculate the mean from from a single file"""

    cdo_command = "cdo tim" + stat

   # run_command(cdo_command, self, silent) 
    run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def time_mean(self, silent = True):
    return(time_stat(self, stat = "mean", silent = silent))

def time_min(self, silent = True):
    return(time_stat(self, stat = "min", silent = silent))

def time_max(self, silent = True):
    return(time_stat(self, stat = "max", silent = silent))

def time_range(self, silent = True):
    return(time_stat(self,jstat = "range", silent = silent))

def time_var(self, silent = True):
    return(time_stat(self, stat = "var", silent = silent))





    
