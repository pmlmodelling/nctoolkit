
import xarray as xr
import os

from ._cleanup import cleanup

def to_xarray(self, decode_times = True, remove = False):
    """convert tracker to xarray data set"""
    ff = self.current
    data = xr.open_dataset(ff, decode_times = decode_times)

    cleanup(keep = self.current)

    if (self.current != self.start) and remove:
        os.remove(self.current)

    return(data)
