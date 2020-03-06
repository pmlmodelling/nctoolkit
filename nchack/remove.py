
import os
from .session import session_info


def nc_remove(ff, deep = False):
    """
    Method for removing netcdf files.
    This is ultra-safe and makes sure the file is in the tmp directory before deleting
    """

    if deep == False:
        if session_info["stamp"] not in ff:
            raise ValueError(f"The file {ff}  was not created during this session")

    if "nchack" not in ff:
        raise ValueError(f"The file {ff}  was not created by nchack")

    if (ff.startswith("/tmp") or ff.startswith("/var/tmp/") or ff.startswith("/usr/tmp/")) == False:
        raise ValueError(f"The file {ff} is not in a tmp folder")

    os.remove(ff)

