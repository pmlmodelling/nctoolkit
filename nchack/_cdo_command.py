
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
from .flatten import str_flatten 
from ._runcommand import run_command

def cdo_command(self, command):
    """ Function to all any cdo command of the the form 'command + infile + outfile'"""

    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(self.target)
    if type(self.current) == list:
        infile = str_flatten(self.current, " ")
    else:
        infile = self.current

    cdo_command = "cdo " + command + " " + infile + " " + self.target

    self.history.append(cdo_command)
    run_command(cdo_command)
    self.history.append(cdo_command)

    self.current = self.target

    cleanup(keep = self.current)


    return(self)



