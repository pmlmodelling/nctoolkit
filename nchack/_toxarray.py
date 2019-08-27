
import copy
import xarray as xr
import os

from ._cleanup import cleanup

def to_xarray(self, decode_times = True):
    """convert tracker to xarray data set"""
    ff = self.current
    data = xr.open_dataset(ff, decode_times = decode_times)

    cleanup(keep = self.current)
    return(data)
