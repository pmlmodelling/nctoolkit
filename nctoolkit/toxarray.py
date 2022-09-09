from datetime import datetime
import xarray as xr


def to_xarray(self, decode_times=True, **kwargs):
    """
    Open a dataset as an xarray object

    Parameters
    -------------
    decode_times: boolean
        Set to False if you do not want xarray to decode the times. Default is True.
        If xarray cannot decode times, CDO will be used.
    **kwargs : kwargs
        Optional arguments to be sent to subset.

    Returns
    ---------------
    to_xarray :  xarray.Dataset

    Examples
    ------------
    If you want to convert a dataset to an xarray dataset, do the following:

    >>> ds.to_xarray()

    This will return an xarray dataset.

    If you do not want time to be decoded, do the following:

    >>> ds.to_xarray(decode_times = False)



    """

    cdo_times = False
    # 3 possibilities:
    #   1: decode_times is False - just open in xarray
    #   2: decode_times is True, and xarray can decodes times -
    #   just open in xarray
    #   3: decode_times is True, but xarray cannot decodes times - open in xarray,
    #   then use cdo to get the times

    # All commands need to be run before opening it xarray
    if len(kwargs) == 0:
        self.run()


    self1 = self.copy()

    if len(kwargs) > 0:
        self1.subset(**kwargs)
        self1.run()

    # if you don't want to decode times, this is straight forward. Just open the data
    if decode_times is False:
        if len(self1) == 1:
            data = xr.open_dataset(self1.current[0], decode_times=decode_times)
        else:
            data = xr.open_mfdataset(self1.current, decode_times=decode_times)
        return data

    # decoding times is trickier, because xarray may fail to do this
    # start by asssuming we don't need to use cdo to work out the times,
    # and figure out if that works

    if cdo_times is False:
        try:
            if len(self1) == 1:
                test = xr.open_dataset(self1.current[0], decode_times=decode_times)
            else:
                test = xr.open_mfdataset(self1.current, decode_times=decode_times)
        except Exception as e:
            cdo_times = True

    # if it does, then just open the data in xarray

    if cdo_times is True and len(self1) > 1:
        raise ValueError("xarray cannot decode times. Set decode_times to False")

    if cdo_times is False:
        if len(self1) == 1:
            data = xr.open_dataset(self1.current[0], decode_times=decode_times)
        else:
            data = xr.open_mfdataset(self1.current, decode_times=decode_times)
        return data

    # If it does not, then we use cdo to pull out the times,
    # then push those to the xarray object

    if len(self1) == 1:

        if isinstance(self1.times[0], datetime):
            times = self1.times
        else:
            times = [
                datetime.strptime(ss.replace("T", " "), "%Y-%m-%d %H:%M:%S")
                for ss in self1.times
            ]

        data = xr.open_dataset(self1.current[0], decode_times=False)
        data = data.assign_coords(time=times)
        return data


def to_dataframe(self, decode_times=True, **kwargs):
    """
    Open a dataset as a pandas data frame

    Parameters
    -------------
    decode_times: boolean
        Set to False if you do not want xarray to decode the times prior to
        conversion to data frame. Default is True.
    **kwargs : kwargs
        Optional arguments to be sent to subset.

    Returns
    ---------------
    to_dataframe :  pandas.DataFrame

    """
    return self.to_xarray(decode_times=decode_times, **kwargs).to_dataframe()
