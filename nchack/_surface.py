
import os
import tempfile
import itertools

from ._filetracker import nc_created
from ._cleanup import cleanup 
from ._runthis import run_this

def surface(self, silent = True):
   # if nc_valid(self.current) == False:
        #raise ValueError("File is invalid")

   # target = tempfile.NamedTemporaryFile().name + ".nc"
   # nc_created.append(target)

    cdo_command = "cdo -sellevidx,1 "
    #cdo_command = "cdo --reduce_dim -sellevidx,1 "
   # run_command(cdo_command, self, silent)
    run_this(cdo_command, self, silent, output = "ensemble")

   # self.history.append(cdo_command)


   # if self.run: self.current = target

    cleanup(keep = self.current)


    return(self)



