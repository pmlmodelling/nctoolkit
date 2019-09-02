
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def ymonstat(self, stat = "mean", silent = True):
    """Function to calculate the seasonal statistic from a function""" 

    cdo_command = "cdo -ymon" + stat

    self.history.append(cdo_command)
    run_this(cdo_command, self, silent, output = "ensemble")

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    

def monthly_mean_climatology(self, silent = True):
    return ymonstat(self, stat = "mean", silent = True)

def monthly_min_climatology(self, silent = True):
    return ymonstat(self, stat = "min", silent = True)

def monthly_max_climatology(self, silent = True):
    return ymonstat(self,  stat = "max", silent = True)
    
def monthly_range_climatology(self, silent = True):
    return ymonstat(self, stat = "range", silent = True)
