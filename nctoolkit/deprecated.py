import pandas as pd
import subprocess
import warnings

from datetime import datetime

from nctoolkit.runthis import run_this
from nctoolkit.session import session_info


def set_missing(self, value=None):
    """
    Set the missing value for a single number or a range

    Parameters
    -------------
    value : 2 variable list or int/float
        If int/float is provided, the missing value will be set to that.
        If a list is provided, values between the two values (inclusive)
        of the list are set to missing.
    """
    warnings.warn("set_missing is deprecated. Please us as_missing")

    if value is None:
        raise ValueError("Please supply missing value")

    if (type(value) is float) or (type(value) is int):
        value = [value, value]

    if type(value) is not list:
        raise TypeError("Please supply a list, int or float!")

    for vv in value:
        if (type(vv) is not float) and (type(vv) is not int):
            raise TypeError(f"{vv} is not an int or float")

    if type(value) is list:
        cdo_command = f"cdo -setrtomiss,{str(value[0])},{str(value[1])}"

    run_this(cdo_command, self, output="ensemble")
