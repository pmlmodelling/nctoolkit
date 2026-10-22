import glob
import os
import threading
import time
import warnings

session_info = dict()
import platform

# macOS needs the `multiprocess` package: the stdlib `multiprocessing` does not
# work with nctoolkit's internals there. Every other module that needs a pool
# or a Manager takes `mp` from here, so the choice is made in one place.
if platform.system() == "Darwin":
    import multiprocess as mp
    from multiprocess.managers import SyncManager
else:
    import multiprocessing as mp
    from multiprocessing.managers import SyncManager

# Pin to the "fork" start method explicitly. These Manager() servers are
# created at bare import time, so on Python 3.14+ (where the Linux default
# start method changed from "fork" to "forkserver") using the default
# context would require re-importing/re-running the __main__ script to
# bootstrap the forkserver -- which re-triggers these same Manager() calls
# recursively and raises RuntimeError before the bootstrap even finishes.
# "fork" never needs that re-import, so it stays safe regardless of how
# nctoolkit is invoked (as a library, or as/from a __main__ script).
_mp_fork_ctx = mp.get_context("fork")


def _exit_with(parent):
    """In a Manager's server: exit once the process that started it is gone
    (a crash or SIGKILL runs no atexit, so nothing else would stop it)."""

    def watch():
        while os.getppid() == parent:
            time.sleep(1)
        os._exit(0)

    threading.Thread(target=watch, daemon=True).start()


def Manager():
    manager = SyncManager(ctx=_mp_fork_ctx)
    manager.start(initializer=_exit_with, initargs=(os.getpid(),))
    return manager


from contextlib import contextmanager


@contextmanager
def fork_pool(cores):
    """
    Context manager giving a fork Pool that is always shut down and joined

    A pool left to the garbage collector is terminated and then joined with no
    timeout, which hangs for ever if a worker survives SIGTERM. The stdlib
    `with Pool()` only terminates, so close/join explicitly here.
    """
    pool = _mp_fork_ctx.Pool(cores)
    try:
        yield pool
    except BaseException:
        pool.terminate()
        pool.join()
        raise
    pool.close()
    pool.join()

nc_safe_par = Manager().list()
temp_dirs_par = Manager().list()
nc_protected_par = Manager().list()

nc_safe = list()


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
        return nc_safe_par[:]
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
        return nc_protected_par[:]
    else:
        return nc_protected


html_files = []

temp_dirs = list()


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
        return temp_dirs_par[:]
    else:
        return temp_dirs


nc_protected = list()
session_warnings = Manager().list()


def get_warnings():
    """
    Function to return a snapshot of the pending warnings

    Manager list proxies have no __iter__, so iterating one runs until the
    manager raises IndexError. On Python 3.12 that exception forms a
    reference cycle that keeps the calling frames, and so DataSets, alive.
    Slicing gives a plain list without that problem.
    """
    return session_warnings[:]


def replay_warnings():
    """
    Issue the queued warnings in this process, and remove them from the queue

    Queue items are (category, text) tuples, not Warning instances: those
    compare by identity, which never survives the pickling that a Manager
    proxy does. Only the items in the snapshot are deleted, so a warning
    appended by a pool worker while this runs is kept for the next replay.
    """
    pending = get_warnings()
    del session_warnings[: len(pending)]
    for category, text in dict.fromkeys(pending):
        warnings.warn(text, category, stacklevel=2)


# cdo processes currently running on behalf of this process, so they can be
# killed if nctoolkit is terminated rather than left running (and writing to
# temp files) after Python has gone
active_cdo = set()


def kill_active_cdo():
    """
    Function to kill any cdo processes started by this process
    """
    import signal

    for proc in list(active_cdo):
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            pass
    active_cdo.clear()


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
