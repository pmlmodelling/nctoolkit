
import tempfile

from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command


def remove_variable(self, vars, silent = True):
    """Function to select the season"""

    target  = tempfile.NamedTemporaryFile().name + ".nc"
    nc_created.append(target)

    if type(vars) is not list:
        vars = [vars]
    vars = str_flatten(vars, ",")
    
    cdo_command = "cdo delete,name=" + vars + " " + self.current + " " + target
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)
    
    if self.run: self.current = target 
    
    cleanup(keep = self.current)
    
    return(self)


