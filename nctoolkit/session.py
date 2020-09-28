import glob
import os


def show_session():
    return session_info


session_info = dict()
nc_safe = []

html_files = []
temp_dirs = set()
temp_files = set()

nc_protected = []


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
