
import os
import tempfile

from .flatten import str_flatten
from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command
from ._runthis import run_this

def select_variables(self, vars = None, silent = True):

    if type(vars) is str:
        vars_list = [vars]
    else:
        vars_list = vars
    vars_list = str_flatten(vars_list, ",")
    
    cdo_command = "cdo selname," + vars_list

    run_this(cdo_command, self, silent, output = "ensemble")
    
    cleanup(keep = self.current)
    
    return(self)
