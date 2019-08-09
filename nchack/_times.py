
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

def times(self):
    ff = self.current
    cdo_result = os.popen( "cdo showtimestamp " + ff).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = pd.Series( (v for v in cdo_result) )
    return(cdo_result)
