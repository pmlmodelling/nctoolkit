import warnings
import numpy as np
from datetime import datetime, timedelta

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this
from nctoolkit.show import nc_years
from nctoolkit.utils import cdo_version, version_above, name_check



def set(self, **kwargs):
    """
    A method for subsetting datasets to specific variables, years, longitudes etc.
    Operations are applied in the order supplied.

    Parameters
    -------------
    *kwargs
        Possible arguments: units, names, long_names 

    """

    non_selected = True

    for key in kwargs:

        if key.lower() in ["unit", "units"]: 
            self.set_units( kwargs[key])
            non_selected = False
        if "long" in key.lower() and "name" in key.lower():
            self.set_longnames( kwargs[key])
            non_selected = False

        if key.lower() == "names":
            self.rename(kwargs[key])
            non_selected = False

    if non_selected:
        raise ValueError("Please provide valid arg to set")
