
from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this

def remove_variable(self, vars, silent = True, cores = 1):
    """Method to remove sellected variables from tracker"""

    if type(vars) is not list:
        vars = [vars]

    vars = str_flatten(vars, ",")
    
    cdo_command = "cdo delete,name=" + vars
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
    #return self
