
import os
import tempfile

from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runcommand import run_command

def vertstat(self, stat = "mean", silent = True):
    """Function to calculate the vertical mean from a function""" 
    ff = self.current

    target = tempfile.NamedTemporaryFile().name + ".nc"

    global nc_created
    nc_created.append(target)

    cdo_command = ("cdo --reduce_dim -vert" + stat + " " + ff + " " + target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self, silent) 
    if self.run: self.current = target 

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
