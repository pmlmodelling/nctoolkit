from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this


def drop(self, vars=None):
    """
    Remove variables
    This will remove stated variables from files in the dataset.

    Parameters
    -------------
    vars : str or list
        Variable or variables to be removed from the dataset.
        Variables that are listed but not in the dataset will be ignored

    Examples
    ------------

    If you wanted to remove a single variable 'var1'  from a dataset data, you would do the following:

    >>> ds.drop('var')

    If you wanted to remove a list of variables, you would do the following:

    >>> ds.drop(['var1', 'var2', 'var2'])


    """

    # Some checks on the validity of variables supplied
    if vars is None:
        raise ValueError("Please supplied vars")

    if type(vars) is not list:
        vars = [vars]

    for vv in vars:
        if type(vv) is not str:
            raise TypeError(f"{vv} is not a str")

    vars = str_flatten(vars, ",")

    # create the cdo command and run it
    cdo_command = f"cdo -delete,name={vars}"
    run_this(cdo_command, self, output="ensemble")
