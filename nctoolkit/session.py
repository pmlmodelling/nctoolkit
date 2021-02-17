import glob
import os
from multiprocessing import Manager


session_info = dict()
mgr = Manager()
nc_safe = list()
nc_safe_par = Manager().list()


def append_safe(ff):
    """
    Function to add a file to the safe list
    """
    if session_info["parallel"]:
        nc_safe_par.append(ff)
    else:
        nc_safe.append(ff)


def remove_safe(ff):
    """
    Function to remove a file to the safe list
    """
    if session_info["parallel"]:
        if ff in nc_safe_par:
            nc_safe_par.remove(ff)
    else:
        if ff in nc_safe:
            nc_safe.remove(ff)


def get_safe():
    """
    Function to get the safe list
    """
    if session_info["parallel"]:
        return list(nc_safe_par)
    else:
        return nc_safe


def append_protected(ff):
    """
    Function to add a file to the protected list
    """
    if session_info["parallel"]:
        nc_protected_par.append(ff)
    else:
        nc_protected.append(ff)


def remove_protected(ff):
    """
    Function to remove a file from the protected list
    """
    if session_info["parallel"]:
        if ff in nc_protected_par:
            nc_protected_par.remove(ff)
    else:
        if ff in nc_protected:
            nc_protected.remove(ff)


def get_protected():
    """
    Function to return the protected list
    """
    if session_info["parallel"]:
        return nc_protected_par
    else:
        return nc_protected


html_files = []

temp_dirs = list()
temp_dirs_par = Manager().list()


def append_tempdirs(ff):
    """
    Function to add a file to the list of temp dirs used
    """
    if session_info["parallel"]:
        if ff not in temp_dirs_par:
            temp_dirs_par.append(ff)
    else:
        if ff not in temp_dirs:
            temp_dirs.append(ff)


def get_tempdirs():
    """
    Function to return the tempdirs in use
    """
    if session_info["parallel"]:
        return temp_dirs_par
    else:
        return temp_dirs


nc_protected = list()
nc_protected_par = Manager().list()


def session_files():
    """
    Function to return the session files
    """
    candidates = []

    for directory in get_tempdirs():
        mylist = [f for f in glob.glob(f"{directory}/*")]
        mylist = [f for f in mylist if session_info["stamp"] in f]
        for ff in mylist:
            candidates.append(ff)

    candidates = list(set(candidates))
    candidates = [x for x in candidates if os.path.exists(x)]

    return candidates
