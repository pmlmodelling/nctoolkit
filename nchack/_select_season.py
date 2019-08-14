
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created


def select_season(self, season):
    """Function to select the season"""

    self.target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    
    cdo_command = "cdo select,season=" + season + " " + self.current + " " + self.target
    self.history.append(cdo_command)
    os.system(cdo_command)
    
    self.current = self.target 
    
    cleanup(keep = self.current)
    
    return(self)
