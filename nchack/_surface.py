
import os
import tempfile
import itertools

from ._filetracker import nc_created
from ._cleanup import cleanup 
from ._runcommand import run_command

def surface(self, silent = True):
   # if nc_valid(self.current) == False:
        #raise ValueError("File is invalid")

    surface_depth = float(nc_depths(self.current)[0])
    target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)

    cdo_command = "cdo --reduce_dim -sellevidx,1 " + self.current + " " + target
    run_command(cdo_command, self, silent)
    self.history.append(cdo_command)


    if self.run: self.current = target

    cleanup(keep = self.current)


    return(self)



