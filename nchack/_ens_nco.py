
import os
import tempfile

from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup
from ._runcommand import run_command

def ensemble_nco(self, method, silent = True):
    """Method to calculate an ensemble stat from a list of files"""
    if self.release == False:
        raise ValueError("NCO methods cannot be held over")

    ff_ensemble = self.current
    if type(ff_ensemble) is not list:
        raise ValueError("The current state of the tracker is not a list")
    target = tempfile.NamedTemporaryFile().name + ".nc"
    owd = os.getcwd()
   # log the full path of the file
    global nc_created
    nc_created.append(target)

    nco_command = ("ncea -y " + method + " " + str_flatten(ff_ensemble, " ") + " " + target) 

    self.history.append(nco_command)
    run_command(nco_command, self, silent) 
    if self.run: self.current = target 

    # clean up the directory
    cleanup(keep = self.current)

#    return self
    

def ensemble_min(self, silent = True):
    """Method to calculate an ensemble min from a list of files"""
    return ensemble_nco(self, "min")

def ensemble_max(self, silent = True):
    """Method to calculate an ensemble max from a list of files"""
    return ensemble_nco(self, "max")

def ensemble_mean(self, silent = True):
    """Method to calculate an ensemble mean from a list of files"""
    return ensemble_nco(self, "mean")




