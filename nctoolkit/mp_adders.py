import pandas as pd
from nctoolkit.api import open_data
import xarray as xr
from matchpoint.utils import get_type


def add_model(self, files=None, map=None, nan=0, precision=None):
    """
    Add model data
    Parameters
    -------------
    files: str or list
        File path(s) of the model data
    map: dict
        Dictionary mapping model variables to validation variables

    nan: float or list
        Value or range of values to set to nan. Defaults to 0.
    precision: numerical precision if needed
        Choose "F64" if advised by a warning

    """

    if self.model is not None:
        raise ValueError("You have already added model data!")

    if type(map) is not dict:
        raise ValueError("You must provided a map")

    if len(map) != 1:
        raise ValueError("There should only be one variable in the map!")

    variable = list(map.keys())[0]

    if self.variable is not None:
        if variable != self.variable:
            raise ValueError("Model and observational variable name")

    self.model = open_data(files, checks=False)

    if len(self.model) > 12:
        print("Checking file times. This could take a minute")
    self.model_map = map
    self.model_nan = nan
    self.model_precision = precision

    # figure out the time dim

    ds1 = open_data(self.model[0])
    pos_times = [
        x
        for x in [
            x for x in list(ds1.to_xarray().dims) if x in list(ds1.to_xarray().coords)
        ]
        if "time" in x
    ]

    if len(pos_times) != 1:
        raise ValueError("Unable to work out the name of time")

    if len(pos_times) == 1:
        time_name = pos_times[0]

    df_times = []

    for ff in self.model:
        ds = xr.open_dataset(ff)
        times = ds[time_name]
        days = [int(x.dt.day) for x in times]
        months = [int(x.dt.month) for x in times]
        years = [int(x.dt.year) for x in times]
        df_times.append(
            pd.DataFrame({"day": days, "month": months, "year": years}).assign(path=ff)
        )
    df_times = pd.concat(df_times)

    if self.obs is not None:
        df_times = self.obs.loc[
            :, ["day", "month", "year"].drop(columns=self.ignore)
        ].merge(df_times.drop(columns=self.ignore))

    files = list(set(df_times.path))
    self.model = open_data(files, checks=False)

    self.model_times = df_times

    self.model_ag = get_type(self.model_times)


def add_depths(self, x=None):
    """
    Add observational data
    Parameters
    -------------
    x:  nctoolkit dataset or list
        If each cell has different vertical levels, this must be provided as a dataset.
        If each cell has the same vertical levels, provide it as a list.

    """

    if type(x) is list:
        self.depths = x

    if type(x) != list:
        if len(x.variables) > 1:
            raise ValueError("Depths file should only have one variable")

        self.depths = x.copy()
        self.depths.rename({x.variables[0]: "depth"})
        self.depths.run()

    self.top = False


def add_observations(self, df=None, map=None):
    """
    Add observational data
    Parameters
    -------------
    df: pandas dataframe

    map: dict
        Dictionary mapping observational variables to validation variables
        This must contain "lon" and "lat" as keys. Optionals: "day", "month", "year", "depth".

    """

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
        raise ValueError("There should only be one model variable")

    variable = [
        x for x in map if x not in ["lon", "lat", "year", "month", "day", "depth"]
    ][0]
    if self.variable is not None:
        if variable != self.variable:
            raise ValueError("Model and observational variable name")

    if self.obs is not None:
        raise ValueError("You have already added observation data!")

    df = df.loc[:, map.values()]
    map_switch = {y: x for x, y in map.items()}
    df = df.rename(columns=map_switch)

    self.obs = df

    self.obs = self.obs.dropna().reset_index(drop=True)

    self.variable = variable
