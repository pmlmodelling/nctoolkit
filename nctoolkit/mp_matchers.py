import pandas as pd
from nctoolkit.api import open_data
import xarray as xr
from nctoolkit.mp_utils import get_type
from nctoolkit.matchpoint import open_matchpoint

def match_points(self, df = None, variables = None, depths = None, tmean = False, top = False, nan = None, regrid = "bil"):
    """
    Match dataset to a spatiotemporal points dataframe
    Parameters
    -------------
    df: pandas dataframe containing the spatiotemporal points to match with.
        The column names must be made up of a subset of "lon", "lat", "year", "month", "day" and "depth"
    variables: str or list
        Str or list of variables. All variables are matched up if this is not supplied.
    depths:  nctoolkit dataset or list giving depths
        If each cell has different vertical levels, this must be provided as a dataset.
        If each cell has the same vertical levels, provide it as a list.
        If this is not supplied nctoolkit will try to figure out what they are.
        Only required if carrying out vertical matchups.
    tmean: bool
        Set to True or False, depending on whether you want temporal averaging at the temporal resolution given by df.
        For example, if you only had months in df, but had daily data in ds, you might want to calculate a daily average in the
        monthly dataset.
        This is equivalent to apply `ds.tmean(..)` to the dataset.
    top: bool
        Set to True if you want only the top/surface level of the dataset to be selected for matching.
    nan: float or list
        Value or range of values to set to nan. Defaults to 0.
        Only required if values in dataset need changed to missing
    regrid: str
        Regridding method. Defaults to "bil". Options available are those in nctoolkit regrid method.
        "nn" for nearest neighbour.

    Returns
    ---------------
    matchpoints : pandas.DataFrame

    """
    self.run()
    ds = self.copy()

    mp = open_matchpoint()

    mp.add_data(x = ds, depths = depths, variables = variables, top = top, nan = nan)
    mp.add_points(df)
    mp.matchup(tmean = tmean, regrid = regrid)
    return mp.values

