
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command

def cell_areas(self):
    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    cdo_command = ( "cdo gridarea " + self.current + " " + self.target)
    self.history.append(cdo_command)
    run_command(cdo_command, self)

    if self.run: self.current = self.target
    cleanup(keep = self.current)
    
    return(self)

