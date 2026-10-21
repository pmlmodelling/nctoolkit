import gc
import weakref

import pytest

import nctoolkit as nc

ff = "data/sst.mon.mean.nc"


@pytest.fixture
def no_gc():
    # with the cyclic collector off, only reference counting can free objects,
    # so anything kept alive by a reference cycle shows up straight away
    gc.collect()
    gc.disable()
    yield
    gc.enable()
    gc.collect()


class Marker:
    pass


def switch_parallel():
    marker = Marker()
    nc.options(parallel=True)
    nc.options(parallel=False)
    return weakref.ref(marker)


def test_options_parallel_does_not_leak_frames(no_gc):
    # iterating a multiprocessing list proxy until IndexError forms a
    # reference cycle that keeps the caller's frame, and its locals, alive
    assert switch_parallel()() is None


def annual_anomaly_ref():
    tracker = nc.open_data(ff, checks=False)
    tracker.annual_anomaly(baseline=[1970, 1979])
    tracker.run()
    return weakref.ref(tracker)


def test_annual_anomaly_dataset_is_freed(no_gc):
    ref = annual_anomaly_ref()
    assert ref() is None
    assert len(nc.session_files()) == 0
