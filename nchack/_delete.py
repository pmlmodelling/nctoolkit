
from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this
from ._variables import variables

def remove_variable(self, vars, silent = True, cores = 1):
    """Function to select the season"""

    if type(vars) is not list:
        vars = [vars]

    actual_vars = self.variables()
    
    for vv in vars:
        if vv not in actual_vars:
            raise ValueError("Variable " + vv + " is not in the file!")

    vars = str_flatten(vars, ",")
    
    cdo_command = "cdo delete,name=" + vars
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
    return self
