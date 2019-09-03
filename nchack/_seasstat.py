
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def seasstat(self, stat = "mean", silent = True, cores = 1):
    """Function to calculate the seasonal statistic from a function""" 

    cdo_command = "cdo -seas" + stat

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def seasonal_mean(self, silent = True, cores = 1):
    return seasstat(self, stat = "mean", silent = True, cores = cores)

def seasonal_min(self, silent = True, cores = 1):
    return seasstat(self, stat = "min", silent = True, cores = cores)

def seasonal_max(self, silent = True, cores = 1):
    return seasstat(self, stat = "max", silent = True, cores = cores)
    
def seasonal_range(self, silent = True, cores = 1):
    return seasstat(self, stat = "range", silent = True, cores = cores)
