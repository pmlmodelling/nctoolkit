
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

def cdo_command(self, command):
    """ Function to all any cdo command of the the form 'command + infile + outfile'"""

    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)

    cdo_command = command + " " + self.current + " " + self.target

    os.system(cdo_command)
    self.history.append(cdo_command)

    self.current = self.target

    cleanup(keep = self.current)


    return(self)



