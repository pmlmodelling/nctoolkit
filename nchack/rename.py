from .runthis import run_this


def rename(self, newnames):
    """
    Rename variables

    Parameters
    -------------
    newnames : dict
        Dictionary with keys being old variable names and values being new variable names
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
