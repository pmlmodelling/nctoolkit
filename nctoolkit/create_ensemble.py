
import copy
import glob
import os
import pandas as pd

# function to find files in directory with a specified variable


def create_ensemble(path="", var=None, recursive=True):
    """
    Generate an ensemble

    Parameters
    -------------
    path: str
        The system to search for netcdf files
    recursive : boolean
        True/False depending on whether you want to search the path recursively. Defaults to True.

    Returns
    -------------
    list
        A list of files
    """

    # make sure the path exists

    if os.path.exists(path) == False:
        raise ValueError("The path provided does not exist!")

    # make sure the path ends with "/" if it is not empty
    if path != "":
        if path.endswith("/") == False:
            path = path + "/"

    if recursive:
        files = [f for f in glob.glob(path + "/**/*.nc", recursive=True)]
    else:
        files = [f for f in glob.glob(path + "*.nc")]

    if len(files) == 0:
        raise ValueError("There is no data in the target directory")

    return files

