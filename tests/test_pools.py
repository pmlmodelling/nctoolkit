import gc
import multiprocessing

import pytest

import nctoolkit as nc

nc.options(lazy=True)


def pool_workers():
    return [
        p for p in multiprocessing.active_children() if p.name.startswith("ForkPoolWorker")
    ]


ensemble = [f"data/ensemble/year195{i}.nc" for i in range(4)]


class TestPools:
    def setup_method(self):
        nc.options(cores=2)

    def teardown_method(self):
        nc.options(cores=1)
        # the caught exceptions' tracebacks keep failed datasets alive in cycles
        gc.collect()

    def test_cdo_ensemble(self):
        ds = nc.open_data(ensemble, checks=False)
        ds.spatial_mean()
        ds.run()
        assert len(ds) == 4
        assert pool_workers() == []

    def test_cdo_ensemble_error(self):
        ds = nc.open_data(ensemble, checks=False)
        ds.cdo_command("selname,not_a_variable")
        with pytest.raises(Exception):
            ds.run()
        del ds
        assert pool_workers() == []

    def test_nco_per_file(self):
        ds = nc.open_data(ensemble, checks=False)
        ds.nco_command("ncks -v sst")
        assert len(ds) == 4
        assert pool_workers() == []

    def test_nco_ensemble(self):
        ds = nc.open_data(ensemble, checks=False)
        ds.nco_command("ncea -y mean", ensemble=True)
        assert len(ds) == 1
        assert pool_workers() == []

    def test_nco_error(self):
        ds = nc.open_data(ensemble, checks=False)
        with pytest.raises(Exception):
            ds.nco_command("ncks -v not_a_variable")
        del ds
        assert pool_workers() == []
