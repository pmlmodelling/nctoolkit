
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command

def cell_areas(self, silent = True):
    target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)
    cdo_command = ( "cdo gridarea " + self.current + " " + target)
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)

    if self.run: self.current = target
    cleanup(keep = self.current)
    
    return(self)

