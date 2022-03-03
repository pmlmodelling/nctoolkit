import os
from nctoolkit.session import session_info, get_tempdirs, get_safe


def nc_remove(ff, deep=False):
    """
    Method for removing netCDF files.
    This is ultra-safe and makes sure the file is in the tmp directory before deleting

    Parameters
    -------------
    deep: bool
        Set to True if you want nctoolkit to be able to delete files created in other sesions.
        Default is False.
    """

    # We need to make sure the file being deleted is from a temporary directory used
    # in the current session. We need to throw an error if it's not
    # Note: this code should be redundant. It is designed as a fail-safe to protect
    # against bugs within nctoolkit causing files to be deleted when they shouldn't be

    unsafe = True

    for directory in get_tempdirs():
        if ff.startswith(directory):
            unsafe = False

    if unsafe:
        raise ValueError(f"The file {ff} is not in a tmp folder")

    # another fail-safe mechanism: ensure nctoolkit is in the file name

    if "nctoolkit" not in ff:
        raise ValueError(f"The file {ff}  was not created by nctoolkit")

    # If things are running in parallel it's possible nc_safe was updated after files to delete
    # were generated....
    if (ff in get_safe()) and (deep is False):
        return None

    if deep is False:
        for ss in list(get_safe()):
            if ss in ff:
                return None

    # another fail-safe mechanism: ensure the session-stamp is in the file name

    if deep is False:
        if session_info["stamp"] not in ff:
            raise ValueError(f"The file {ff}  was not created during this session")

    # if things are going in parallel, it's possible the file will have been deleted by another process
    # so use simple exception handling in case this has happend

    # If things are in parallel, it's safer to add a delay here
    try:
        os.remove(ff)
    except:
        x = "1"
