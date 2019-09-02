
import os
import tempfile
import itertools

from ._filetracker import nc_created
from ._cleanup import cleanup 
from ._runthis import run_this

def surface(self, silent = True):

    cdo_command = "cdo -sellevidx,1 "

    run_this(cdo_command, self, silent, output = "ensemble")

    cleanup(keep = self.current)

    return(self)



