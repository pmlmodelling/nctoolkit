import os

from nctoolkit.session import session_info, nc_safe, temp_dirs, temp_files, get_safe
import warnings


def nc_remove(ff, deep=False):
    """
    Method for removing netcdf files.
    This is ultra-safe and makes sure the file is in the tmp directory before deleting
    """

    unsafe = True

    for directory in temp_dirs:
        if ff.startswith(directory):
            unsafe = False

    if unsafe:
        raise ValueError(f"The file {ff} is not in a tmp folder")

    if "nctoolkit" not in ff:
        raise ValueError(f"The file {ff}  was not created by nctoolkit")

    # If things are running in parallel it's possible nc_safe was updated after files to delete
    # were generated....
    if (ff in get_safe()) and (deep is False):
        return None

    if deep is False:
        if session_info["stamp"] not in ff:
            raise ValueError(f"The file {ff}  was not created during this session")

    try:
        os.remove(ff)
    except:
        x = "1"
