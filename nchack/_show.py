
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command

def show_years(self):

    cdo_result = os.popen( "cdo showyear " + self.current).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = pd.Series( (v for v in cdo_result) )
    return(cdo_result)
