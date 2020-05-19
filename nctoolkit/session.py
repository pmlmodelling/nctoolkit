
import glob
import os


def show_session():
    return session_info


session_info = dict()
nc_safe = []

html_files = []

nc_protected = []


def session_files():

    candidates = []

    mylist = [f for f in glob.glob("/tmp/*.*")]
    mylist = mylist + [f for f in glob.glob("/var/tmp/*.*")]
    mylist = [f for f in mylist if session_info["stamp"] in f]
    for ff in mylist:
        candidates.append(ff)

    candidates = list(set(candidates))
    candidates = [x for x in candidates if os.path.exists(x)]

    return candidates
