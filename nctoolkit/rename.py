from nctoolkit.runthis import run_this


def rename(self, newnames):
    """
    Rename variables in a dataset

    Parameters
    -------------
    newnames : dict
        Dictionary with key-value pairs being original and new variable names

    Examples
    ------------
    If you want to rename a variable x to y, do the following:

        >>> ds.rename({"x":"y"})

    """

    # check a dict was supplied
    if type(newnames) is not dict:
        raise TypeError("a dictionary was not supplied")

    # now, we need to loop through the renaming dictionary to get the cdo sub
    cdo_rename = ""

    for key, value in newnames.items():
        if type(key) is not str:
            raise TypeError(f"{key} is not a str")
        if type(value) is not str:
            raise TypeError(f"{value} is not a str")
        cdo_rename += "," + key
        cdo_rename += "," + value

    # create the cdo call and run it
    cdo_command = "cdo -chname" + cdo_rename
    run_this(cdo_command, self, output="ensemble")
