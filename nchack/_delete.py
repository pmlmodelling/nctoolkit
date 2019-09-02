
import tempfile

from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command
from ._runthis import run_this


def remove_variable(self, vars, silent = True):
    """Function to select the season"""

    if type(vars) is not list:
        vars = [vars]
    vars = str_flatten(vars, ",")
    
    cdo_command = "cdo delete,name=" + vars
    run_this(cdo_command, self, silent, output = "ensemble")
    
    cleanup(keep = self.current)
    
    return(self)


