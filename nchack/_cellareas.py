
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._cleanup import cleanup
from ._filetracker import nc_created

def cellareas(self, remove = True):
    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    cdo_call = ( "cdo gridarea " + self.current + " " + self.target)
    self.history.append(cdo_call)
    os.system(cdo_call)
    if self.current != self.start and remove:
        os.remove(self.current)
    self.current = self.target
    cleanup(keep = self.curren)
    
    return(self)

