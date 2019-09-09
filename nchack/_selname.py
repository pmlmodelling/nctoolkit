
from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this
from ._variables import variables

def select_variables(self, vars = None, silent = True, cores = 1):
    """Method to select variables from a netcdf file"""

    if type(vars) is str:
        vars_list = [vars]
    else:
        vars_list = vars

    valid_vars = self.variables()

    for vv in vars_list:
        if vv not in valid_vars:
            raise ValueError(vv + " is not available in the file!")

    vars_list = str_flatten(vars_list, ",")
    
    cdo_command = "cdo selname," + vars_list

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
    return self
