
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def monstat(self,  stat = "mean", silent = True):
    """Function to calculate the monthly statistic from a netcdf file""" 
    cdo_command = "cdo -mon" + stat

    run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def monthly_mean(self, silent = True):
    return monstat(self, stat = "mean", silent = silent)

def monthly_min(self, silent = True):
    return monstat(self, stat = "min", silent = silent)

def monthly_max(self, silent = True):
    return monstat(self, stat = "max", silent = silent)
    
def monthly_range(self, silent = True):
    return monstat(self, stat = "range", silent = silent)
