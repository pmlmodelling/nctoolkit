
# to do
# think about adding ability to call nco
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runcommand import run_command

def ensemble_percentile(self, p = 50, silent = True):
    """Function to calculate an ensemble percentile from a list of files"""
    ff_ensemble = self.current

    if type(ff_ensemble) is not list:
        raise ValueError("The current state of the tracker is not a list")

    target = tempfile.NamedTemporaryFile().name + ".nc"
    owd = os.getcwd()

   # log the full path of the file
    global nc_created
    nc_created.append(target)

    cdo_command = ("cdo enspctl," + str(p) + " " + str_flatten(ff_ensemble, " ") + " " + target) 

    self.history.append(cdo_command)
    run_command(cdo_command, self, silent) 
    if self.run: self.current = target 

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    
