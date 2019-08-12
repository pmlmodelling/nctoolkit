
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._cleanup import cleanup
from ._filetracker import nc_created

def cellareas(self):
    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    cdo_call = ( "cdo gridarea " + self.current + " " + self.target)
    self.history.append(cdo_call)
    os.system(cdo_call)

    self.current = self.target
    cleanup(keep = self.current)
    
    return(self)

