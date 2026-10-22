import os
import signal
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHILD = """
import os, signal
import nctoolkit as nc
from nctoolkit.session import mp

print("PIDS " + " ".join(str(p.pid) for p in mp.active_children()), flush=True)
{body}
"""

KILL = "os.kill(os.getpid(), signal.SIGKILL)"


def run_child(body):
    proc = subprocess.run(
        [sys.executable, "-c", CHILD.format(body=body)],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    line = [l for l in proc.stdout.splitlines() if l.startswith("PIDS ")][0]
    return [int(p) for p in line.split()[1:]]


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    # a zombie awaiting reaping by init still answers signal 0
    try:
        with open(f"/proc/{pid}/stat") as f:
            return f.read().rsplit(")", 1)[1].split()[0] != "Z"
    except OSError:
        return True


def wait_gone(pids, timeout=5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not any(alive(p) for p in pids):
            return True
        time.sleep(0.2)
    return not any(alive(p) for p in pids)


def test_sigkill_leaves_no_manager_servers():
    pids = run_child(KILL)
    assert len(pids) > 0
    assert wait_gone(pids)


def test_normal_exit_leaves_no_manager_servers():
    pids = run_child("")
    assert len(pids) > 0
    assert wait_gone(pids)


def test_parallel_ensemble_still_works():
    body = """
nc.options(cores=2)
ens = nc.open_data(["data/sst.mon.mean.nc"] * 3, checks=False)
ens.merge("time")
ens.subset(timesteps=0)
ens.run()
print("OK", ens.variables, flush=True)
"""
    proc = subprocess.run(
        [sys.executable, "-c", CHILD.format(body=body)],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    assert "OK" in proc.stdout
