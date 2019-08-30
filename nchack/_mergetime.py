
# to do
# think about adding ability to call nco

import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runthis import run_this

def merge_time(self, silent = True):
    """Function to calculate an ensemble range from a list of files"""
    ff_ensemble = self.current

    if type(ff_ensemble) is not list:
        raise ValueError("The current state of the tracker is not a list")

    target = tempfile.NamedTemporaryFile().name + ".nc"

   # log the full path of the file
    global nc_created
    nc_created.append(target)

    cdo_command = ("cdo mergetime ")

    self.history.append(cdo_command)
    run_this(cdo_command, self, silent, output = "one") 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    
