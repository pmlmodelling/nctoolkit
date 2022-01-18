from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this


def drop(self, **kwargs):
    """
    Remove variables
    This will remove stated variables from files in the dataset.

    Parameters
    -------------
    *kwargs
        Possible arguments: var, year, month, day 

        Note: this uses partial matches. So years, month, variable etc. will also work

    Each kwarg works as follows:

    var: str or list
        A variable or list of variables to select. This method will accept wild cards.
        So using 'var*' would select all variables beginning with 'var'.
    day : list, range or int
        Day(s) to select.
    month : list, range or int
        Month(s) to select.
    year : list, range or int
        Year(s) to select.

    Examples
    ------------

    If you wanted to remove a single variable 'var1'  from a dataset data, you would do the following:

    >>> ds.drop(variable = 'var')

    If you wanted to remove a list of variables, you would do the following:

    >>> ds.drop(variable = ['var1', 'var2', 'var2'])

    If you wanted to remove the 29th Feburary you would do the following: 

    >>> ds.drop(month = 2, day = 29) 


    """

    if len(kwargs) == 0:
        raise ValueError("Please provide terms to drop")

    valids = ["var", "mon", "day", "year"]


    for key in kwargs:
        key_check = 0
        for vv in valids:
            if vv in key:
                key_check += 1
        if key_check > 1 or key_check == 0:
            raise ValueError("Drop term is invalid or ambiguous")

    temporal_command = "cdo -delete"

    for key in kwargs:

        if "var" in key:
            vars = kwargs[key]

            if type(vars) is not list:
                vars = [vars]

            for vv in vars:
                if type(vv) is not str:
                    raise TypeError(f"{vv} is not a str")

            vars = str_flatten(vars, ",")

            # create the cdo command and run it
            cdo_command = f"cdo -delete,name={vars}"
            run_this(cdo_command, self, output="ensemble")

        if ("mon" in key) or ("day" in key) or ("year" in key):
            vars = kwargs[key]

            if type(vars) is not list:
                vars = [vars]

            for vv in vars:
                if type(vv) is not int:
                    raise TypeError(f"{vv} is not a int")

            vars = str_flatten(vars, ",")


            # create the cdo command and run it
            if "day" in key:
                temporal_command = temporal_command + f",day={vars}"
            if "mon" in key:
                temporal_command = temporal_command + f",month={vars}"
            if "year" in key:
                temporal_command = temporal_command + f",year={vars}"

        
    if len(temporal_command) > len("cdo -delete"):
        run_this(temporal_command, self, output="ensemble")


