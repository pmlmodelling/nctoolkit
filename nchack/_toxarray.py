import xarray as xr
from ._cleanup import cleanup

def to_xarray(self, decode_times = True):
    """
    Open a dataset as an xarray object

    Parameters
    -------------
    decode_times: boolean
        Set to False if you do not want xarray to decode the times. Default is True. 

    """
    
    if type(self.current) is str:
        data = xr.open_dataset(self.current, decode_times = decode_times)
    else:   
        data = xr.open_mfdataset(self.current, decode_times = decode_times)

    cleanup(keep = self.current)
    return data
