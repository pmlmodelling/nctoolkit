
import os
import tempfile

from ._filetracker import nc_created
from ._cleanup import cleanup 
from ._runcommand import run_command

def nco_command(self, command):
    """ Function to all any nco command of the the form 'command + infile + outfile'"""
    target = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)
    nco_command = command + " " + self.current + " " + target
    run_command(nco_command)
    self.history.append(ndo_command)

    if self.run: self.current = target

    cleanup(keep = self.current)

    return(self)



