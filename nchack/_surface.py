
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._depths import nc_depths
from ._clip import clip
from ._filetracker import nc_created

def surface(self, vars = None, remove = True):
   # if nc_valid(self.current) == False:
        #raise ValueError("File is invalid")

    surface_depth = float(nc_depths(self.current)[0])

    self.clip(vars = vars, vert_range= [surface_depth, surface_depth])

    return(self)



