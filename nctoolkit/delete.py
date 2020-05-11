# The warnings in this method could be improved slightly. Possibly case of using mutate/transmute that will make warnings less tiday
# Though CDO should always pick issues up


from .flatten import str_flatten
from .runthis import run_this
from .show import nc_variables
import warnings


def remove_variables(self, vars=None):
    """
    Remove variables

    Parameters
    -------------
    vars : str or list
        Variable or variables to be removed from the data set. Variables that are listed but not in the dataset will be ignored
    """

    if vars is None:
        raise ValueError("Please supplied vars")

    if type(vars) is not list:
        vars = [vars]

    for vv in vars:
        if type(vv) is not str:
            raise TypeError(f"{vv} is not a str")

    orig_vars = []
    for ff in self:
        orig_vars += nc_variables(ff)

    missing_vars = [vv for vv in vars if vv not in orig_vars]

    vars = [vv for vv in vars if vv in orig_vars]

    if len(vars) == 0:
        warnings.warn(message="None of the variables supplied are in the dataset")
        return None
    else:
        if len(missing_vars) > 0:
            if len(missing_vars) > 1:
                warnings.warn(
                    message=f"{str_flatten(missing_vars)} are not in the dataset!"
                )
            else:
                warnings.warn(
                    message=f"{str_flatten(missing_vars)} is not in the dataset!"
                )

    vars = str_flatten(vars, ",")

    # create the cdo command and run it
    cdo_command = f"cdo -delete,name={vars}"
    run_this(cdo_command, self, output="ensemble")
