import nctoolkit as nc
import subprocess
import platform
import pandas as pd
import glob
import xarray as xr
import os, pytest
import random

nc.options(lazy=True)




ff = "data/sst.mon.mean.nc"


class TestTemp:
    def test_temp(self):
        with pytest.raises(TypeError):
            nc.temp_file.temp_file(1)

        if platform.system() == "Linux":
            candidates = []
            for directory in nc.session.get_tempdirs():
                mylist = [f for f in glob.glob(f"{directory}/*")]
                for ff in mylist:
                    candidates.append(ff)
        
            mylist = [f for f in candidates if "nctoolkit" in f and nc.session.session_info["stamp"] not in f]

            if len(mylist) == 0:
            

                import random
                rf = random.randint(1,10000000)
                temp1 = f"/tmp/nctoolk{rf}chnctoolkittmpjs7aia2j.nc"
                rf = random.randint(1,10000000)
                temp2 = f"/tmp/nctoolk{rf}chnctoolkittmpjs7aia2j.nc"
                os.mknod(temp1)
                os.mknod(temp2)

                assert os.path.exists(temp1)
                assert os.path.exists(temp2)
        
                nc.deep_clean()

                assert os.path.exists(temp1) == False
                assert os.path.exists(temp2) == False
