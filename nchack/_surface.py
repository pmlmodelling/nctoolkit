
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._depths import nc_depths
from ._clip import clip
from ._filetracker import nc_created
from ._cleanup import cleanup 
from ._runcommand import run_command

def surface(self, vars = None):
   # if nc_valid(self.current) == False:
        #raise ValueError("File is invalid")

    surface_depth = float(nc_depths(self.current)[0])
    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)

    cdo_command = "cdo --reduce_dim -sellevidx,1 " + self.current + " " + self.target
    run_command(cdo_command, self)
    self.history.append(cdo_command)

    self.target

    if self.run: self.current = self.target

    cleanup(keep = self.current)


    return(self)



