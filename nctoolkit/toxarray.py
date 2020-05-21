from datetime import datetime
import xarray as xr
from nctoolkit.cleanup import cleanup


def to_xarray(self, decode_times=True):
    """
    Open a dataset as an xarray object

    Parameters
    -------------
    decode_times: boolean
        Set to False if you do not want xarray to decode the times. Default is True. If xarray cannot decode times, CDO will be used.

    """
    ## 3 possibilities:
    ##   1: decode_times is False - just open in xarray
    ##   2: decode_times is True, and xarray can decodes times - just open in xarray
    ##   3: decode_times is True, but xarray cannot decodes times - open in xarray, then use cdo to get the times

    # All commands need to be run before opening it xarray
    self.run()

    # if you don't want to decode times, this is straight forward. Just open the data
    if decode_times is False:
        if type(self.current) is str:
            data = xr.open_dataset(self.current, decode_times=decode_times)
        else:
            data = xr.open_mfdataset(self.current, decode_times=decode_times)
        return data

    # decoding times is trickier, because xarray may fail to do this
    # start by asssuming we don't need to use cdo to work out the times, and figure out if that works
    cdo_times = False

    try:
        if type(self.current) is str:
            test = xr.open_dataset(self.current, decode_times=decode_times)
        else:
            test = xr.open_mfdataset(self.current, decode_times=decode_times)
    except:
        cdo_times = True

    # if it does, then just open the data in xarray

    if cdo_times is False:
        if type(self.current) is str:
            data = xr.open_dataset(self.current, decode_times=decode_times)
        else:
            data = xr.open_mfdataset(self.current, decode_times=decode_times)
        return data

    # If it does not, then we use cdo to pull out the times, then push those to the xarray object

    if type(self.current) is str:

        times = [
            datetime.strptime(ss.replace("T", " "), "%Y-%m-%d %H:%M:%S")
            for ss in self.times
        ]

        data = xr.open_dataset(self.current, decode_times=False)
        data = data.assign_coords(time=times)
        return data

    else:
        data = xr.open_mfdataset(self.current, decode_times=decode_times)
        return data



def to_dataframe(self, decode_times=True):
    """
    Open a dataset as a pandas data frame

    Parameters
    -------------
    decode_times: boolean
        Set to False if you do not want xarray to decode the times prior to conversion to data frame. Default is True.

    """
    # everything must be run first
    self.run()
    return self.to_xarray(decode_times=decode_times).to_dataframe()
