
import xarray as xr
import pandas as pd
import numpy as np
import os
import tempfile
import itertools

from ._cleanup import cleanup
from ._filetracker import nc_created
from ._runcommand import run_command

def expression(self, operations = None, method = "expr"):
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

    self.target = tempfile.NamedTemporaryFile().name + ".nc"
    
    nc_created.append(self.target)

    cdo_call = ("cdo " + method + "," + expr + " " + self.current  + " " + self.target)
    self.history.append(cdo_call)
    run_command(cdo_call)

    if os.path.isfile(self.target) == False:
        raise ValueError("Application of expr did not work. Check output")

    self.current = self.target
    
    cleanup(keep = self.current)    
    

    return(self)


def mutate(self, operations = None):
    return(expression(self, operations = operations, method = "expr"))


def transmute(self, operations = None):
    return(expression(self, operations = operations, method = "aexpr"))



