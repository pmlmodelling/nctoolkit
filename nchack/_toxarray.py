
import copy
import xarray as xr
import os

from ._cleanup import cleanup

def to_xarray(self, decode_times = True):
    """convert tracker to xarray data set"""
    
    if type(self.current) is str:
        data = xr.open_dataset(self.current, decode_times = decode_times)
    else:   
        data = xr.open_mfdataset(self.current, decode_times = decode_times)

    cleanup(keep = self.current)
    return(data)
