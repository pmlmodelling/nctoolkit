import glob
import os
from multiprocessing import Manager


def show_session():
    return session_info


session_info = dict()
mgr = Manager()
nc_safe = list()
nc_safe_par = Manager().list()


def append_safe(ff):
    if session_info["parallel"]:
        nc_safe_par.append(ff)
    else:
        nc_safe.append(ff)

def remove_safe(ff):
    if session_info["parallel"]:
        if ff in nc_safe_par:
            nc_safe_par.remove(ff)
    else:
        if ff in nc_safe:
            nc_safe.remove(ff)

def get_safe():
    if session_info["parallel"]:
        return list(nc_safe_par)
    else:
        return nc_safe

def append_protected(ff):
    if session_info["parallel"]:
        nc_protected_par.append(ff)
    else:
        nc_protected.append(ff)

def remove_protected(ff):
    if session_info["parallel"]:
        if ff in nc_protected_par:
            nc_protected_par.remove(ff)
    else:
        if ff in nc_protected:
            nc_protected.remove(ff)

def get_protected():
    if session_info["parallel"]:
        return nc_protected_par
    else:
        return nc_protected



html_files = []

temp_dirs = list()
temp_dirs_par = Manager().list()

def append_tempdirs(ff):
    if session_info["parallel"]:
        if ff not in temp_dirs_par:
            temp_dirs_par.append(ff)
    else:
        if ff not in temp_dirs:
            temp_dirs.append(ff)

def get_tempdirs():
    if session_info["parallel"]:
        return temp_dirs_par
    else:
        return temp_dirs

#nc_protected = []
nc_protected = list()
nc_protected_par = Manager().list()


def session_files():

    candidates = []

    for directory in get_tempdirs():
        mylist = [f for f in glob.glob(f"{directory}/*")]
        mylist = [f for f in mylist if session_info["stamp"] in f]
        for ff in mylist:
            candidates.append(ff)

    candidates = list(set(candidates))
    candidates = [x for x in candidates if os.path.exists(x)]

    return candidates
