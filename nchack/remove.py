import os
from .session import session_info
from .session import nc_safe


def nc_remove(ff, deep=False):
    """
    Method for removing netcdf files.
    This is ultra-safe and makes sure the file is in the tmp directory before deleting
    """

    if (
        ff.startswith("/tmp")
        or ff.startswith("/var/tmp/")
        or ff.startswith("/usr/tmp/")
    ) == False:
        raise ValueError(f"The file {ff} is not in a tmp folder")

    if "nchack" not in ff:
        raise ValueError(f"The file {ff}  was not created by nchack")

    if (ff in nc_safe) and (deep == False):
        raise ValueError(f"The file {ff} is in the safe list, so cannot be removed")

    if deep == False:
        if session_info["stamp"] not in ff:
            raise ValueError(f"The file {ff}  was not created during this session")

    os.remove(ff)
