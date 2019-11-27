from .flatten import str_flatten
from .runthis import run_this

def remove_variables(self, vars):
    """
    Remove variables

    Parameters
    -------------
    vars : str or list
        Variable or variables to be removed from the data set
    """

    if type(vars) is not list:
        vars = [vars]

    vars = str_flatten(vars, ",")

    cdo_command = "cdo -delete,name=" + vars
    run_this(cdo_command, self, output = "ensemble")


