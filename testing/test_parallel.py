import nctoolkit as nc
import platform
import subprocess
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


ff = "data/sst.mon.mean.nc"

import time
import os
def process_chain(ff):
    ds = nc.open_data(ff)
    ds.spatial_mean()
    ds.run()
    #time.sleep(0.1)
    x =  os.path.exists(ds[0])

    del ds
    nc.cleanup()
    return x

#class TestPar:
if True:
    #def test_parallel(self):
    def test_parallel():
        ff = "data/sst.mon.mean.nc"
        tracker = nc.open_data(ff)
        n = len(nc.session_files())
        assert n == 0

        #if platform.system() == "Linux":
        nc.options(cores = 2)
        tracker = nc.open_data(ff)
        tracker.split("year")
        tracker.tmean()
        tracker.merge("time")
        tracker.tmean()
        tracker.spatial_mean()
        x = tracker.to_dataframe().sst[0].astype("float")


        tracker = nc.open_data(ff)
        tracker.tmean("year")
        tracker.tmean()
        tracker.spatial_mean()
        y = tracker.to_dataframe().sst[0].astype("float")

        assert x == y

        for ff in nc.session.get_safe():
            nc.session.remove_safe(ff)

        data = nc.open_data("data/ensemble/*.nc")
        data.spatial_sum(by_area = True)
        data.run()

        if platform.system() == "Linux":
            import multiprocessing as mp
        else:
           import multiprocess as mp
        nc.options(parallel = True)
        n_cores = mp.cpu_count()
        ensemble = nc.open_data("data/ensemble/*.nc")

        ensemble = nc.create_ensemble("data/ensemble")
        target_list = []
        results = dict()
        pool = mp.Pool(n_cores)
        for ff in ensemble:
            temp = pool.apply_async(process_chain, [ff])
            results[ff] = temp
        pool.close()
        pool.join()
        for k, v in results.items():
            target_list.append(v.get())
        if len([x for x in target_list if x == False]) > 0:
            raise ValueError("This test failed")


        nc.options(parallel = False)


        nc.options(cores = 1)


test_parallel()



