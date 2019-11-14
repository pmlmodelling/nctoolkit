
from ._runthis import run_this

def rename(self, newnames):
    """
    Rename variables

    Parameters
    -------------
    newnames : dict
        Dictionary with keys being old variable names and values being new variable names

    """

    if type(newnames) is not dict:
        raise ValueError("a dictionary was not supplied")

    # now, we need to loop through the renaming dictionary to get the cdo sub
    cdo_rename = ""

    for key, value in newnames.items():
        cdo_rename +=  "," + key
        cdo_rename += "," + value

    # need a check at this point for file validity
    cdo_command= "cdo -chname" + cdo_rename

    run_this(cdo_command, self, output = "ensemble")


