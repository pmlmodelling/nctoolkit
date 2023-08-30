from nctoolkit.show import nc_variables
from nctoolkit.utils import name_check
import warnings


# A custom format for warnings.
def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + "\n"


warnings.formatwarning = custom_formatwarning


def rename(self, newnames=None, **kwargs):
    """
    rename: Rename variables in a dataset

    Parameters
    -------------
    newnames : dict
        Dictionary with key-value pairs being original and new variable names
    * kwargs
        Alternative method for renaming

    Examples
    ------------
    If you want to rename a variable x to y, do the following:

        >>> ds.rename({"x":"y"})

    Alternatively, you could do the following:

        >>> ds.rename(x="y")

    """

    if newnames is None and len(kwargs) > 0:
        newnames = dict()
        for kk in kwargs:
            newnames[kwargs[kk]] = kk

    # check a dict was supplied
    if not isinstance(newnames, dict):
        raise TypeError("a dictionary was not supplied")

    if len(self.history) == len(self._hold_history):
        variables = nc_variables(self[0])
        for key in newnames:
            if key not in variables:
                if len(self) > 1:
                    warnings.warn(
                        message=f"{key} is not in the first file of the dataset"
                    )
                else:
                    warnings.warn(message=f"{key} is not in the dataset")

    # now, we need to loop through the renaming dictionary to get the cdo sub
    cdo_rename = ""

    for key, value in newnames.items():
        if not isinstance(key, str):
            raise TypeError(f"{key} is not a str")
        if not isinstance(value, str):
            raise TypeError(f"{value} is not a str")
        if name_check(key) is False:
            raise ValueError(f"{key} is not a valid netCDF variable name")

        if name_check(value) is False:
            raise ValueError(f"{value} is not a valid netCDF variable name")

    for key, value in newnames.items():
        cdo_rename += "," + key
        cdo_rename += "," + value

    # create the cdo call and run it
    cdo_command = "-chname" + cdo_rename
    self.cdo_command(cdo_command, ensemble=False)
