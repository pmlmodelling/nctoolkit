
from .runthis import run_this

def arithall(self, stat = "divc", x = None):
    """Method to calculate the spatial stat from a netcdf"""

    #cdo_command = "cdo --reduce_dim -fld" + stat
    cdo_command = "cdo -" + stat + "," + str(x)

    run_this(cdo_command, self,  output = "ensemble")


def divide_by_constant(self, x):
    """
    Divide all variables by a constant

    Parameters
    ------------
    x : float or int
    """

    return arithall(self, stat = "divc", x = x)


def add_constant(self, x):
    """
    Add a constant to all variables

    Parameters
    ------------
    x : float or int
    """

    return arithall(self, stat = "addc", x = x)


def subtract_constant(self, x):
    """
    Subtract a constant from all variables

    Parameters
    ------------
    x : float or int
    """

    return arithall(self, stat = "subc", x = x)


def multiply_by_constant(self, x):
    """
    Multiply all variables by a constant

    Parameters
    ------------
    x : float or int
    """

    return arithall(self, stat = "mulc", x = x)



