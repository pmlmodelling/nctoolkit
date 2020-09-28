import os

from nctoolkit.session import session_info, nc_safe, temp_dirs, temp_files


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

    if (ff in nc_safe) and (deep is False):
        raise ValueError(f"The file {ff} is in the safe list, so cannot be removed")

    possibles = [os.path.basename(x) for x in temp_files]
    if os.path.basename(ff) not in possibles:
        raise ValueError(f"{ff} is not a temp file created by nctoolkit")

    if deep is False:
        if session_info["stamp"] not in ff:
            raise ValueError(f"The file {ff}  was not created during this session")

    os.remove(ff)
