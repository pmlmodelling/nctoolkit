
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command

def expression(self, operations = None, method = "expr", silent = True):
    """Function to mutate a netcdf file using expr"""

    if type(operations) is not dict:
        raise ValueError("No expression was provided")

    # first,we need to convert the operations dictionary to a cdo expression 

    expr = []
    for key,value in operations.items():
        expr.append(key + "=" + value)
        
    expr = ";".join(expr)
    expr = expr.replace("(", "\\(")
    expr = expr.replace(")", "\\)")
    expr = expr.replace(" ", "" )
    expr = '"' + expr + '"'

    target = tempfile.NamedTemporaryFile().name + ".nc"
    
    nc_created.append(target)

    cdo_command = ("cdo " + method + "," + expr + " " + self.current  + " " + target)
    self.history.append(cdo_command)
    run_command(cdo_command, self, silent)

    if self.run: self.current = target
    
    cleanup(keep = self.current)    
    

    return(self)


def mutate(self, operations = None, silent = True):
    return(expression(self, operations = operations, method = "expr", silent = silent))


def transmute(self, operations = None, silent = True):
    return(expression(self, operations = operations, method = "aexpr", silent = silent))



