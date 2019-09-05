
import os
import tempfile
import itertools

from ._filetracker import nc_created
from ._cleanup import cleanup 
from ._runthis import run_this

def bottom(self, silent = True, cores = 1):
    """Method to extract the bottom level from netcdf files"""

    if type(self.current) is list:
        ff = self.current[0]
        print("warning: first file in ensemble used to determine number of vertical levels")
    else:
        ff = self.current

    n_levels = int(os.popen( "cdo nlevel " + ff).read().split("\n")[0])
    
    # First, we need to get the number of levels 
    cdo_command = "cdo -sellevidx," + str(n_levels)

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    cleanup(keep = self.current)

    return(self)



