
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runcommand import run_command

def monstat(self,  stat = "mean", silent = True):
    """Function to calculate the monthly statistic from a netcdf file""" 
    ff = self.current

    target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(target)

    cdo_command = ("cdo -mon" + stat + " " + ff + " " + target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self, silent) 
    if self.run: self.current = target 

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
