
# to do
# think about adding ability to call nco

import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def ensemble_range(self, silent = True):
    """Function to calculate an ensemble range from a list of files"""

    if type(self.current) is not list:
        raise ValueError("The current state of the tracker is not a list")

    cdo_command = "cdo ensrange " 

    run_this(cdo_command, self, silent, output = "one")

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    
