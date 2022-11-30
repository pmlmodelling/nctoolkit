import pandas as pd
import re
import scipy.interpolate as interpolate
import warnings
import numpy as np
from nctoolkit.api import open_data, open_thredds
from tqdm import tqdm


from scipy.interpolate import interp1d

def extrap1d(interpolator, max_extrap = 5):
    xs = interpolator.x
    ys = interpolator.y

    def pointwise(x):
        if x > xs[-1]  and x <= xs[-1] + max_extrap:
            return ys[-1]
        elif x > (xs[-1] + max_extrap):
            return np.nan
        elif x >= (xs[0] - max_extrap) and x < xs[0]:
            return ys[0]
        elif x < (xs[0] - max_extrap):
            return np.nan
        else:
            return interpolator(x)

    def ufunclike(xs):
        return np.array(list(map(pointwise, np.array(xs))))

    return ufunclike

def interp(x,y, levels, max_extrap = 5):
    try:
        f_i = interp1d(x, y)
        f_x = extrap1d(f_i, max_extrap = max_extrap)
        #f = interpolate.interp1d(x, y, fill_value = "extrapolate")
        return f_x(levels)
    except:
        df = pd.DataFrame({"x":x, "y":y}).dropna()
        new = []
        for x in levels:
            if float(np.abs(df.x - x)) < max_extrap:
                new.append(df.y)
            else:
                new.append(np.nan)
        return new


def matchup(self,  tmean = False, regrid = "bil", max_extrap = 5):
    """
    Matchup gridded model and point observational data
    
    Parameters
    -------------
    tmean: bool
        Set to True or False. Defaults to False. This will calculate a temporal mean for the dataset at the
        resolution given in the point dataset. So, for example, if the point data is monthly, but the dataset
        is daily, it will calculate an appropritate monthly mean.
    regrid: str
        Regridding method. Defaults to "bil". Options available are those in nctoolkit regrid method.
        "nn" for nearest neighbour.
    max_extrap: float
        Maximum distance for vertical extrapolation of values 

    """

    if max_extrap < 0:
        raise ValueError("max_extrap must be positive")

    self.max_extrap = max_extrap

    if self.depths is not None:
        if "depth" not in self.points.columns:
            print("Depths were supplied, but are not in df")
            self.depths = None

    on = None

    new_on = [x for x in self.points.columns if x in ["day", "month", "year"]]

    if len(new_on) > 0:
        on = new_on

    #  loop through all time steps in the observational df....

    # Figure out which points in the dataframe are actually in the dataframe...

    if on is None:
        tmean = False

    points = self.points

    if isinstance(on, str):
        on = [on]

    if on is not None:
        if isinstance(on, list):
            for x in ["day", "month", "year"]:
                if x not in on and x in points.columns:
                    points = points.drop(columns = x)


    if self.thredds:
        ds = open_thredds(self.data[0], checks = False)
    else:
        ds = open_data(self.data[0], checks = False)

    ds.subset(variables = ds.variables[0])
    ds.subset(time = 0)
    ds.top()
    ds.cdo_command("setmisstoc,1")
    df = points.loc[:,["lon", "lat"]].drop_duplicates()
    ds.regrid(df, method = regrid)
    grid = ds.to_dataframe().reset_index().dropna().loc[:,["lon", "lat"]].drop_duplicates()

    n_start = len(points)

    points = points.merge(grid)

    if len(points) == 0:
        raise ValueError("None of the points are contained within the dataset grid")

    if len(points) < n_start:
        n_remove = n_start - len(points)
        print(f"{n_remove} points are outside the dataset grid, and were therefore removed.")


    n_levels = len(self.data.levels)

    if self.points_temporal is False:
        if self.temporal:
            if on is None:
                on = ["all"]
                print("Points will be matched for all time steps")

    if on is None:
        if self.temporal is True:
            raise ValueError("You have not provided an on argument")

    acceptable = ["lon", "lat", "year", "month", "day", "depth"]

    if self.temporal is False:
        # We need a quick hack
        df_times = []
        for ff in self.data:
            df_times.append(pd.DataFrame({"year":[None]}))
        df_times = pd.concat(df_times)
        self.data_times = df_times


    if self.temporal:
        if on != ["all"]:
            if tmean is False:
                df_times = self.data_times
                point_col = [x for x in df_times.columns if x in points.columns]
                df_times = self.data_times.merge(points.loc[:,point_col]).drop_duplicates()
            else:

                if on == ["day"]:
                    on = ["day", "month"]
                    if "month" not in points.columns:
                        on.remove("month")
                if not isinstance(on, list):
                    raise ValueError("on must be a list")
                for x in on:
                    if x not in ["day", "month", "year", "all"]:
                        raise ValueError(f"{x} is not a valid")

                for x in ["day", "month", "year"]:
                    if x not in on:
                        if x in points.columns:
                            points = points.drop(columns=x)

                # This needs to work when there is no time

                if self.points_temporal:
                    df_times = self.data_times.loc[:, on].merge(points.loc[:, on])
                else:
                    df_times = self.data_times
                df_times = df_times.drop_duplicates()
                time_avail = [x for x in ["year", "month", "day"] if x in df_times.columns]
                df_times = df_times.sort_values(by=time_avail).reset_index(drop=True)
        else:
            df_times = self.data_times.drop(columns = "path")

    if self.temporal is False:
        df_times = self.data_times

    df_merged = []


    # depths only need to be calculated once
    if self.depths is not None:
        if not isinstance(self.depths, list):
            ds_depths = self.depths.copy()
            obs_locs = points.loc[:,["lon", "lat"]]
            ds_depths.regrid(obs_locs, method = regrid) 
            df_depths = (
                ds_depths.to_dataframe()
                .reset_index()
                .loc[:, ["lon", "lat", "depth"]]
                .drop_duplicates()
            )
        else:
            df_depths = pd.DataFrame({"depth": self.depths})

        all_depths = df_depths

    points_merged = False
    if self.points_temporal is False:
        if len(self.data.levels) < 2:
            if self.thredds:
                ds = open_thredds(self.data, checks = False)
            else:
                ds = open_data(self.data, checks = False)
            if self.variables is not None:
                ds.subset(variables = self.variables)
            ds.regrid(points.loc[:,["lon", "lat"]], method = regrid) 
            df_merged = [ds.to_dataframe().reset_index()]
            points_merged = True

    n_missing = 0


    if (len(df_times)) == 0:
        raise ValueError("There are no matching times")


    if points_merged is False:

        df_times = df_times.sample(frac = 1)

        print("Looping through times in ds and df to matchup")
        for i in tqdm(range(0, len(df_times))):
            if self.temporal:
                i_df = df_times.iloc[
                    i : (i + 1) :,
                ]
                i_df = i_df.reset_index(drop = True)
                if self.points_temporal:
                    i_grid = points.merge(i_df).loc[:, ["lon", "lat"]]
                else:
                    i_grid = points.loc[:,["lon", "lat"]]
                i_year = None
                i_month = None
                i_day = None
                if "year" in on or tmean is False:
                    try:
                        i_year = i_df.year.values[0]
                    except:
                        i_year = None
                if "month" in on or tmean is False:
                    try:
                        i_month = i_df.month.values[0]
                    except:
                        i_month = None
                if "day" in on or tmean is False:
                    try:
                        i_day = i_df.day.values[0]
                    except:
                        i_day = None

                if on == ["all"]:
                    try:
                        i_year = i_df.year.values[0]
                    except:
                        i_year = None
                    try:
                        i_month = i_df.month.values[0]
                    except:
                        i_month = None
                    try:
                        i_day = i_df.day.values[0]
                    except:
                        i_day = None

                if self.thredds:
                    ds = open_thredds(set(self.data_times.merge(i_df).path), checks=False)
                else:
                    ds = open_data(set(self.data_times.merge(i_df).path), checks=False)
            else:
                if self.thredds:
                    ds = open_thredds(self.data, checks=False)
                else:
                    ds = open_data(self.data, checks=False)
                i_grid = points.loc[:, ["lon", "lat"]].drop_duplicates()


            if self.variables is not None:
                ds.subset(variables=self.variables)
            if self.top:
                ds.top()

            if self.temporal:
                for opt in ["day", "year", "month"]:
                    if i_day is not None:
                        ds.subset(day=i_day)
                    if i_month  is not None:
                        ds.subset(month=i_month)
                    if i_year is not None:
                        ds.subset(year=i_year)

                    if self.points_temporal:
                        if len(ds) > 1:
                            ds.merge("time")
            if on is not None and tmean is True:
                ds.tmean(on)

            if self.data_nan is not None:
                ds.as_missing(self.data_nan)

            ds.regrid(i_grid, method = regrid) 

            df_model = ds.to_dataframe().reset_index().drop_duplicates()

            # figure out the time dim

            if self.temporal:
                pos_times = [
                    x
                    for x in [
                        x
                        for x in list(ds.to_xarray().dims)
                        if x in list(ds.to_xarray().coords)
                    ]
                    if "time" in x
                ]

                if len(pos_times) != 1:
                    raise ValueError("Unable to work out the name of time")

                if len(pos_times) == 1:
                    time_name = pos_times[0]

            if self.depths is  None:

                if self.temporal:
                    locs = [time_name, "lon", "lat"]
                else:
                    locs = [ "lon", "lat"]

                locs += ds.variables
                if len(ds.levels) > 1:
                    adict = dict(ds.to_xarray().dims)

                    locs += [k for k in adict.keys() if adict[k]  == n_levels]
                    acceptable += [k for k in adict.keys() if adict[k]  == n_levels]
                    locs = list(set(locs))

                df_model = df_model.loc[
                    :,  locs
                ].drop_duplicates()
                df_merged.append(df_model)

            else:

                if "deptht" in df_model.columns:

                    if self.temporal:
                        locs = [time_name, "lon", "lat", "deptht"]
                    else:
                        locs = [ "lon", "lat", "deptht"]
                    locs += ds.variables
                    df_model = df_model.loc[:, locs].drop_duplicates()

                else:
                    locs = [ "lon", "lat"]
                    locs += ds.variables
                    drop = [x for x in df_model.columns if "depth" in x and "bnds" not in x]
                    locs += drop
                    df_model = df_model.loc[ :, locs ].drop_duplicates()
                    df_model = df_model.drop(columns = drop)


                if self.points_temporal:
                    i_obs_df = i_df.merge(points)
                else:
                    i_obs_df = points

                i_obs_locs = i_obs_df.loc[:, ["lon", "lat"]].drop_duplicates()
                

                if True:

                    for j in range(0, len(i_obs_locs)):
                        if self.depths is not None:
                            df_depths = df_depths

                        j_obs = i_obs_locs.iloc[j : (j + 1), :].merge(i_obs_df).drop_duplicates()

                        j_model = (
                            df_model.merge(j_obs.loc[:, ["lon", "lat"]].drop_duplicates())
                            .reset_index(drop=True)
                        )
                        j_model = j_model.reset_index(drop = True)

                        if len(j_model) > 0:
                            if not isinstance(self.depths, list):
                                if self.depths is not None:
                                    j_depths = (
                                        df_depths.merge(j_obs.loc[:, ["lon", "lat"]])
                                        .drop_duplicates()
                                        .reset_index(drop=True)
                                    )
                                    locs = ["lon_x", "lon_y", "depth"]
                                    locs += ds.variables

                                    j_model = j_model.merge(
                                        j_depths, left_index=True, right_index=True
                                    ).loc[:, locs]
                            else:
                                if self.depths is not None:
                                    locs = ["lon", "lat", "depth"]
                                    locs += ds.variables
                                    j_model = j_model.merge(
                                        df_depths, left_index=True, right_index=True
                                    ).loc[:, locs]
                                    #j_model = j_model.drop_duplicates()

                            if self.depths is not None:
                                max_depth = np.max(j_model.depth)
                                min_depth = np.min(j_model.depth)

                            if len(j_obs) > 0:

                                try:
                                    if self.depths is not None:
                                        i_var = 0
                                        for var in ds.variables:
                                            j_obs[var] = interp(list(j_model.depth), j_model[var], list(j_obs.depth), max_extrap = self.max_extrap)
        
                                            i_var +=1
                                        for x in ["day", "month", "year"]:
                                            if x in i_df.columns:
                                                j_obs[x] = i_df[x].values[0]

                                        df_merged.append(j_obs)
                                    else:
                                        df_merged.append(j_model)
                                except:
                                    n_missing += 1

    if n_missing > 0:
        warnings.warn(f"{n_missing} points did not have sufficient vertical points in ds for vertical interpolation")

    if len(df_merged) == 0:
        raise ValueError("No data matches were found")

    self.values = df_merged
    df_merged = pd.concat(df_merged).drop_duplicates().reset_index(drop=True)

    if self.temporal is False:
        acceptable += ds.variables
        acceptable = [x for x in df_merged.columns if x in acceptable]
        df_merged = df_merged.loc[:,acceptable]

    if len([x for x in df_merged.columns if x.startswith("time")]) == 1:
        orig_df = df_merged
        try:
            time_name = [x for x in df_merged.columns if x.startswith("time")][0]
            times = df_merged[time_name]
            df_merged["year"] = [x.year for x in times]
            df_merged["month"] = [x.month for x in times]
            df_merged["day"] = [x.day for x in times]
            df_merged = df_merged.drop(columns = time_name)
            # get acceptable variables....
            acceptable += ds.variables
            acceptable = [x for x in df_merged.columns if x in acceptable]
            df_merged = df_merged.loc[:,acceptable]

        except:
            df_merged = orig_df

    if "path" in df_merged.columns:
        df_merged = df_merged.drop(columns = "path")

    self.values = df_merged


