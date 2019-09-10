
from .flatten import str_flatten
from ._cleanup import cleanup
from ._runthis import run_this
from ._variables import variables
from ._variables import nc_variables

def remove_variable(self, vars, silent = True, cores = 1):
    """Function to select the season"""

    if type(vars) is not list:
        vars = [vars]

   # if type(self.current) is str:
   #     file_list = [self.current]
   # else:
   #     file_list = self.current
  
   # for ff in file_list:
   #     valid_vars = nc_variables(ff)
   #     for vv in vars:
   #         if vv not in valid_vars:
   #             raise ValueError(vv + " is not available in " + ff)

    vars = str_flatten(vars, ",")
    
    cdo_command = "cdo delete,name=" + vars
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)
    
    #return self
