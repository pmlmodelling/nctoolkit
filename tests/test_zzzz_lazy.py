import pandas as pd
import xarray as xr
import os, pytest

import importlib
import nctoolkit as nc

ff = "data/sst.mon.mean.nc"


class TestFinal:
    def test_cleanall(self):
        from shutil import copyfile
        copyfile("tests/.nctoolkitrc", ".nctoolkitrc")
        importlib.reload(nc.api)

        print(nc.session.session_info)
        os.remove(".nctoolkitrc")


        assert nc.session.session_info["lazy"] == True
        assert nc.session.session_info["cores"] == 6
        assert nc.session.session_info["thread_safe"] == True
        assert nc.session.session_info["user"] == "me"
        assert nc.session.session_info["password"] == "pass"
        assert nc.session.session_info["precision"] == "F32"

        from os.path import expanduser
        home = expanduser("~")

        importlib.reload(nc.api)

        assert nc.session.session_info["lazy"] == False

        print(nc.session.session_info)

        copyfile("tests/.nctoolkitrc", home+"/.nctoolkitrc")
        importlib.reload(nc.api)

        assert nc.session.session_info["lazy"] == True
        assert nc.session.session_info["cores"] == 6
        assert nc.session.session_info["thread_safe"] == True
        assert nc.session.session_info["user"] == "me"
        assert nc.session.session_info["password"] == "pass"
        assert nc.session.session_info["precision"] == "F32"

        os.remove( home+"/.nctoolkitrc")


