
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

def surface(self, vars = None, remove = True):
   # if nc_valid(self.current) == False:
        #raise ValueError("File is invalid")

    surface_depth = float(nc_depths(self.current)[0])
    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)

    cdo_command = "cdo sellevidx,1 " + self.current + " " + self.target
    os.system(cdo_command)
    self.history.append(cdo_command)

    self.target
    if self.current != self.start and remove:
        os.remove(self.current)
    self.current = self.target

    cleanup(keep = self.current)


    return(self)



