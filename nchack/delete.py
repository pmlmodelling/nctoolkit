from .flatten import str_flatten
from .runthis import run_this
import warnings

def remove_variables(self, vars):
    """
    Remove variables

    Parameters
    -------------
    vars : str or list
        Variable or variables to be removed from the data set. Variables that are listed but not in the dataset will be ignored
    """

    if type(vars) is not list:
        vars = [vars]

    missing_vars = [vv for vv in vars if vv not in self.variables]

    vars = [vv for vv in vars if vv in self.variables]

    if len(vars) == 0:
        warnings.warn(message = "None of the variables supplied are in the dataset")
        return None
    else:
        if len(missing_vars) > 0:
            if len(missing_vars) > 1:
                warnings.warn(message = str_flatten(missing_vars) + " are not in the dataset!")
            else:
                warnings.warn(message = str_flatten(missing_vars) + " is not in the dataset!")

    vars = str_flatten(vars, ",")

    # create the cdo command and run it
    cdo_command = "cdo -delete,name=" + vars
    run_this(cdo_command, self, output = "ensemble")


