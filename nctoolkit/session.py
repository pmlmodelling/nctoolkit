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
        return nc_safe_par
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
temp_dirs = set()

#nc_protected = []
nc_protected = list()
nc_protected_par = Manager().list()


def session_files():

    candidates = []

    for directory in temp_dirs:
        mylist = [f for f in glob.glob(f"{directory}/*")]
        mylist = [f for f in mylist if session_info["stamp"] in f]
        for ff in mylist:
            candidates.append(ff)

    candidates = list(set(candidates))
    candidates = [x for x in candidates if os.path.exists(x)]

    return candidates
