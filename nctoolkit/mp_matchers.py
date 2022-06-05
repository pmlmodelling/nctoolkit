import pandas as pd
from nctoolkit.api import open_data
import xarray as xr
from nctoolkit.mp_utils import get_type
from nctoolkit.matchpoint import open_matchpoint

def match_points(self, df = None, depths = None):
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

    Returns
    ---------------
    matchpoints : pandas.DataFrame

    """
    self.run()
    ds = self.copy()

    mp = open_matchpoint()

    mp.add_data(x = ds, depths = depths)
    mp.add_points(df)
    mp.matchup()
    return mp.values

