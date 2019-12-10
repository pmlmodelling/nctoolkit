import xarray as xr
from datetime import datetime



def to_xarray(self, decode_times = True):
    """
    Open a dataset as an xarray object

    Parameters
    -------------
    decode_times: boolean
        Set to False if you do not want xarray to decode the times. Default is True.

    """

    self.release()

    if decode_times is False:
        if type(self.current) is str:
            data = xr.open_dataset(self.current, decode_times = decode_times)
        else:
            data = xr.open_mfdataset(self.current, decode_times = decode_times)
        return data

    cdo_times = True
    try:
        x = xr.open_dataset(self.current)
        cdo_times = False
    except:
        cdo_times = True

    if cdo_times is False:
        if type(self.current) is str:
            data = xr.open_dataset(self.current, decode_times = decode_times)
        else:
            data = xr.open_mfdataset(self.current, decode_times = decode_times)
        return data

    # get the times

    if type(self.current) is str:

        times = [datetime.strptime(ss.replace("T", " "), '%Y-%m-%d %H:%M:%S') for ss in self.times()]

        data = xr.open_dataset(self.current, decode_times = False)
        data = data.assign_coords(time = times)
        return data

    else:
        data = xr.open_mfdataset(self.current, decode_times = decode_times)
        return data





