import nctoolkit as nc

nc.options(lazy=True)
import gc
import os

from nctoolkit.session import nc_safe, nc_safe_par


class TestSafeLists:
    def test_parallel_toggle_moves_every_file(self):
        # removing items from a list while looping over it skipped every other
        # file, leaving half of them unprotected while parallel mode was on
        assert nc.session.session_info["parallel"] == False
        fake = ["A", "B", "C", "D", "E", "F"]
        nc_safe.extend(fake)

        nc.options(parallel=True)
        assert sorted(nc_safe_par) == fake
        assert [ff for ff in nc_safe if ff in fake] == []

        nc.options(parallel=False)
        assert sorted(ff for ff in nc_safe if ff in fake) == fake
        assert list(nc_safe_par) == []

        for ff in fake:
            nc_safe.remove(ff)
        assert nc.session.session_info["parallel"] == False

    def test_annual_anomaly_keeps_shared_files(self):
        # annual_anomaly switches to parallel mode internally; the round trip
        # used to drop references to files shared by copies of a dataset, so
        # the original's file was deleted once the copies were collected
        assert nc.session.session_info["parallel"] == False
        n = len(nc.session_files())
        assert n == 0

        ds = nc.open_data("data/sst.mon.mean.nc", checks=False)
        ds.subset(years=range(1970, 1990))
        ds.run()
        shared = ds[0]

        keep = [ds.copy(), ds.copy()]
        tracker = ds.copy()
        tracker.annual_anomaly(baseline=[1970, 1974])
        tracker.run()
        assert nc.session.session_info["parallel"] == False

        del keep, tracker
        gc.collect()
        nc.cleanup()

        assert os.path.exists(shared)
        assert ds.years == list(range(1970, 1990))

        del ds
        gc.collect()
        nc.cleanup()
        assert len(nc.session_files()) == 0
