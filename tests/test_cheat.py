import pandas as pd
import xarray as xr
import os, pytest

import importlib
import nctoolkit as nc
import platform



class TestFinal:
    def test_cheat(self):

        # only run this test on linux
        if platform.system() == "Linux":
            import textract
            assert len(nc.session_files()) == 0
            assert len(nc.session.get_safe()) == 0
            ff = "../cheatsheet/nctoolkit_cheatsheet.pdf"
            assert len(nc.session_files()) == 0
            assert len(nc.session.get_safe()) == 0
            ff = "cheatsheet/nctoolkit_cheatsheet.pdf"
# read p    df ff
            text = textract.process(ff, method='pdfminer')
            text = text.decode('utf-8')
            # version format is v*.*.*. Find it in text
            import re
            pattern = re.compile(r'v\d+\.\d+\.\d+')
            version = pattern.search(text)
            version = version.group()
            version = version.replace("v", "")
            the_version = nc.__version__
            assert version == the_version


