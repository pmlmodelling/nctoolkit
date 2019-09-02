
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def seasstat(self, stat = "mean", silent = True):
    """Function to calculate the seasonal statistic from a function""" 

    cdo_command = "cdo -seas" + stat

    run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def seasonal_mean(self, silent = True):
    return seasstat(self, stat = "mean", silent = True)

def seasonal_min(self, silent = True):
    return seasstat(self, stat = "min", silent = True)

def seasonal_max(self, silent = True):
    return seasstat(self, stat = "max", silent = True)
    
def seasonal_range(self, silent = True):
    return seasstat(self, stat = "range", silent = True)
