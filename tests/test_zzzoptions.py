import nctoolkit as nc
import pandas as pd
import glob
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff1 = "data/2003.nc"
ff2 = "data/2004.nc"


class TestApi2:
    def test_errors(self):

        valid_keys = ["thread_safe", "lazy", "cores", "precision", "temp_dir", "parallel", "checks", "progress"]

        nc.options(thread_safe = True)
        assert nc.session.session_info["thread_safe"] == True

        nc.options(cores = 2)
        assert nc.session.session_info["cores"] == 2
        nc.options(cores = 1)
        assert nc.session.session_info["cores"] == 1

        nc.options(lazy = False)
        assert nc.session.session_info["lazy"] == False

        nc.options(lazy = True)
        assert nc.session.session_info["lazy"] == True

        nc.options(precision = "I16")
        assert nc.session.session_info["precision"] == "I16"

        nc.options(precision = "default")
        assert nc.session.session_info["precision"] == None 

        nc.options(temp_dir = "/var/tmp")
        assert nc.session.session_info["temp_dir"] == "/var/tmp"
        nc.options(temp_dir = "/tmp")
        assert nc.session.session_info["temp_dir"] == "/tmp"

        nc.options(checks = False)
        assert nc.session.session_info["checks"] == False
        nc.options(checks = True)
        assert nc.session.session_info["checks"] == True

        nc.options(progress = "on")
        assert nc.session.session_info["progress"] == "on"
        nc.options(progress = "auto")
        assert nc.session.session_info["progress"] == "auto"


        with pytest.raises(ValueError):
            nc.options(progress = "asdfu") 

        with pytest.raises(ValueError):
            nc.options(precision = "asdfu") 

        with pytest.raises(ValueError):
            nc.options(cores = 1000) 
