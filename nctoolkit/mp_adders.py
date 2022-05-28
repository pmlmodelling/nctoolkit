import pandas as pd
from nctoolkit.api import open_data
import xarray as xr
from nctoolkit.mp_utils import get_type


def add_data(self, x=None, variables=None, depths = None, nan=None, top = False):
    """
    Add dataset for matching
    Parameters
    -------------
    x: nctoolkit dataset or str/list of file paths
        Dataset or file(s) to match up with 
    variables: str or list
        Str or list of variables. All variables are matched up if this is not supplied.
    depths:  nctoolkit dataset or list giving depths
        If each cell has different vertical levels, this must be provided as a dataset.
        If each cell has the same vertical levels, provide it as a list.
        Only required if carrying out vertical matchups.
    nan: float or list
        Value or range of values to set to nan. Defaults to 0.
        Only required if values in dataset need changed to missing
    top: bool 
        Set to True if you want only the top/surface level of the dataset to be selected for matching.

    """

    if depths is not None:
        self.add_depths(depths)

    if depths is None:
        if self.points is not None:
            if "depth" in self.points:
                raise ValueError("You cannot match depths without supplying dataset depths")

    self.top = top

    if self.data is not None:
        raise ValueError("You have already added data!")

    if variables is None:
        print("All variables will be used")

    self.data = open_data(x) 

    if len(self.data) > 12:
        print("Checking file times. This could take a minute")

    self.data_nan = nan

    # figure out the time dim

    ds1 = open_data(self.data[0])
    pos_times = [
        x
        for x in [
            x for x in list(ds1.to_xarray().dims) if x in list(ds1.to_xarray().coords)
        ]
        if "time" in x
    ]

    if len(pos_times) != 1:
        print("Unable to work out the name of time. Assuming no temporal matchups can occur.")
        self.temporal = False

    if self.temporal:

        if len(pos_times) == 1:
            time_name = pos_times[0]

        df_times = []

        for ff in self.data:
            ds = xr.open_dataset(ff)
            times = ds[time_name]
            days = [int(x.dt.day) for x in times]
            months = [int(x.dt.month) for x in times]
            years = [int(x.dt.year) for x in times]
            df_times.append(
                pd.DataFrame({"day": days, "month": months, "year": years}).assign(path=ff)
            )
        df_times = pd.concat(df_times)

        if self.points is not None:
            df_times = self.points.loc[
                :, ["day", "month", "year"].drop(columns=self.ignore)
            ].merge(df_times.drop(columns=self.ignore))

        x = list(set(df_times.path))
    self.data = open_data(x, checks = False) 

    self.variables = variables

    if self.temporal:
        self.data_times = df_times
    else:
        self.data_times = None 

    if self.temporal is False:
        if len(self.data) > 1:
            raise ValueError("You cannot provide more than one dataset without temporal information")



def add_depths(self, x=None):
    """
    Add depth 
    Parameters
    -------------
    x:  nctoolkit dataset or list/iterable
        If each cell has different vertical levels, this must be provided as a dataset.
        If each cell has the same vertical levels, provide it as a list.

    """

    if self.depths is not None:
        raise ValueError("You have already provided depths")

    if "api.DataSet" not in str(type(x)):
        self.depths = [y for y in x]

    if type(x) != list:
        if len(x.variables) > 1:
            raise ValueError("Depths file should only have one variable")

        self.depths = x.copy()
        self.depths.rename({x.variables[0]: "depth"})
        self.depths.run()


def add_points(self, df=None, map=None, **kwargs):
    """
    Add point data
    Parameters
    -------------
    df: pandas dataframe containing the spatiotemporal points to match with.

    map: dict
        Dictionary mapping point location variables to required or optional dimensions.
        This must contain "lon" and "lat" as keys. Optionals: "day", "month", "year", "depth".
        As an alternative, these can be provided as kwargs, i.e. lon = .., lat = ..., etc.

    """

    self.points_temporal = False

    if len(kwargs) > 0 and map is None:
        map = dict(kwargs)

    if map is None:
        raise ValueError("Please provide a map. Starting sugestion: {'lon':'lon', 'lat':'lat', 'depth':'depth','year':'year','month':'month','day':'day'}.")

    for x in ["year", "month", "day"]:
        if x in map:
            self.points_temporal = True

    if type(map) is not dict:
        raise ValueError("You must provided a map")

    for x in ["year", "month", "day", "depth"]:
        if x not in map:
            print(f"Warning: You have not provided {x} in map")

    for x in ["lon", "lat"]:
        if x not in map:
            raise ValueError(f"Please provide {x} in map")

    if (
        len(
            [
                x
                for x in map.keys()
                if x not in ["lon", "lat", "year", "month", "day", "depth"]
            ]
        )
        > 1
    ):
        raise ValueError("You have provided an invalid map")

    if self.points is not None:
        raise ValueError("You have already added observation data!")

    df = df.loc[:, map.values()]
    map_switch = {y: x for x, y in map.items()}
    df = df.rename(columns=map_switch)

    self.points = df

    self.points = self.points.dropna().reset_index(drop=True)

    if self.depths is None and self.data is not None:
        if self.points is not None:
            if "depth" in self.points:
                raise ValueError("You cannot match depths without supplying dataset depths")

