import glob
import os
import signal
import subprocess
import sys
import time

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHILD = """
import sys, time
import nctoolkit as nc
from nctoolkit.session import session_info

nc.options(parallel={parallel})
ds = nc.open_data("data/sst.mon.mean.nc", checks=False)
ds.subset(timesteps=0)
ds.run()
print("STAMP " + session_info["stamp"], flush=True)
{body}
"""

SLEEP = "time.sleep(60)"

# a slow cdo is simulated with a shim that sleeps instead of writing output
SLOW_CDO = """
import nctoolkit.runners as r
orig = r.run_shell
def slow(command):
    return orig("sleep 60; " + command)
r.run_shell = slow
ds2 = nc.open_data("data/sst.mon.mean.nc", checks=False)
ds2.subset(timesteps=1)
print("BUSY", flush=True)
ds2.run()
"""


def start_child(body=SLEEP, parallel=False, new_group=False):
    code = CHILD.format(body=body, parallel=parallel)
    proc = subprocess.Popen(
        [sys.executable, "-c", code],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        text=True,
        start_new_session=new_group,
    )
    stamp = None
    deadline = time.time() + 90
    for line in proc.stdout:
        if line.startswith("STAMP "):
            stamp = line.split()[1]
            break
        if time.time() > deadline:
            break
    assert stamp is not None, "child never reported its session stamp"
    if "BUSY" in body or "slow" in body:
        for line in proc.stdout:
            if line.startswith("BUSY"):
                break
        time.sleep(1)
    return proc, stamp


def leftovers(stamp):
    return [
        f
        for d in ("/tmp", "/var/tmp")
        for f in glob.glob(f"{d}/*{stamp}*")
    ]


def finish(proc, stamp):
    """Make sure a test never leaks files or processes whatever happens."""
    if proc.poll() is None:
        proc.kill()
    proc.wait()
    for f in leftovers(stamp):
        os.remove(f)


@pytest.mark.parametrize("sig", [signal.SIGTERM, signal.SIGHUP, signal.SIGINT])
def test_signal_exits_and_cleans(sig):
    proc, stamp = start_child()
    try:
        assert len(leftovers(stamp)) > 0
        proc.send_signal(sig)
        proc.wait(timeout=15)
        assert leftovers(stamp) == []
        if sig != signal.SIGINT:
            # the process must still die from the signal it was sent
            assert proc.returncode == -sig
    finally:
        finish(proc, stamp)


def test_normal_exit_cleans():
    proc, stamp = start_child(body="")
    try:
        proc.wait(timeout=30)
        assert leftovers(stamp) == []
    finally:
        finish(proc, stamp)


def test_sigterm_while_cdo_running_kills_cdo():
    proc, stamp = start_child(body=SLOW_CDO)
    try:
        proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=15)
        time.sleep(1)
        assert leftovers(stamp) == []
        # the "sleep 60; cdo ..." shell started for the operation must be gone
        out = subprocess.run(
            ["pgrep", "-f", f"sleep 60; cdo .*{stamp}"],
            stdout=subprocess.PIPE,
            text=True,
        )
        assert out.stdout.strip() == ""
    finally:
        finish(proc, stamp)


def test_parallel_mode_group_sigterm_cleans():
    # SIGTERM to the whole process group also kills the Manager servers behind
    # the parallel-mode session lists
    proc, stamp = start_child(parallel=True, new_group=True)
    try:
        assert len(leftovers(stamp)) > 0
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(timeout=15)
        assert leftovers(stamp) == []
    finally:
        finish(proc, stamp)


def test_existing_sigterm_handler_is_chained():
    # installed *before* nctoolkit is imported so nctoolkit has to chain to it
    code = (
        "import signal, sys, time\n"
        "signal.signal(signal.SIGTERM, lambda s, f: (print('APP', flush=True), sys.exit(3)))\n"
        + CHILD.format(body=SLEEP, parallel=False)
    )
    proc = subprocess.Popen(
        [sys.executable, "-c", code], cwd=ROOT, stdout=subprocess.PIPE, text=True
    )
    stamp = None
    try:
        for line in proc.stdout:
            if line.startswith("STAMP "):
                stamp = line.split()[1]
                break
        assert stamp is not None
        proc.send_signal(signal.SIGTERM)
        out = proc.stdout.read()
        proc.wait(timeout=15)
        assert "APP" in out
        assert proc.returncode == 3
        assert leftovers(stamp) == []
    finally:
        finish(proc, stamp or "no-stamp-found")
