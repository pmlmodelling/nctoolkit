
import os

from nctoolkit.session import session_info, nc_safe


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

    if "nctoolkit" not in ff:
        raise ValueError(f"The file {ff}  was not created by nctoolkit")

    if (ff in nc_safe) and (deep == False):
        raise ValueError(f"The file {ff} is in the safe list, so cannot be removed")

    if deep == False:
        if session_info["stamp"] not in ff:
            raise ValueError(f"The file {ff}  was not created during this session")

    os.remove(ff)
