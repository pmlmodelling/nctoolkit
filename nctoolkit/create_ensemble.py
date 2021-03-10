import glob
import os

# function to find files in directory with a specified variable


def create_ensemble(path="", recursive=True):
    """
    Generate an ensemble

    Parameters
    -------------
    path: str
        The directory to search for netCDF files
    recursive : boolean
        True/False depending on whether you want to search the path recursively.
        Defaults to True.

    Returns
    -------------
    list
        A list of files

    Examples
    ------------

    If you wanted to recursively find all netCDF files available in a directory "data", you would do this:

    >>> import nctoolkit as nc
    >>> nc.create_ensemble("data")

    If you wanted to find the files in that directory and ignore subdirectories, you would instead do this:

    >>> nc.create_ensemble("data", recursive = False)


    """

    # make sure the path exists

    if os.path.exists(path) is False:
        raise ValueError("The path provided does not exist!")

    # make sure the path ends with "/" if it is not empty
    if path != "":
        if path.endswith("/") is False:
            path = path + "/"

    if recursive:
        files = [f for f in glob.glob(path + "/**/*.nc*", recursive=True)]
    else:
        files = [f for f in glob.glob(path + "*.nc*")]

    if len(files) == 0:
        raise ValueError("There is no data in the target directory")

    return files
