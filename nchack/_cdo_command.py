
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._clip import clip
from ._filetracker import nc_created
from ._cleanup import cleanup 
from .flatten import str_flatten 
from ._runthis import run_this

def cdo_command(self, command, silent = True):
    """ Function to all any cdo command of the the form 'command + infile + outfile'"""

    if type(self.current) == list:
        infile = str_flatten(self.current, " ")
    else:
        infile = self.current

    cdo_command = "cdo " + command

    run_this(cdo_command, self, silent, output = "ensemble")

    cleanup(keep = self.current)

    return(self)



