import pandas as pd
import re
import scipy
import numpy as np
from nctoolkit.api import open_data
from nctoolkit.mp_utils import get_type


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_equation(x):
    regexp = re.compile(r"[+,\-,/, \* ]")
    return len(regexp.findall(x)) > 0


def get_timedf(x):
    times = x.times

    model_times_df = pd.DataFrame(
        {
            "year": [x.year for x in times],
            "month": [x.month for x in times],
            "day": [x.day for x in times],
        }
    )
    return model_times_df


def matchup(self, on=None):
    """
    Matchup gridded model and point observational data
    Parameters
    -------------
    on: list or string
        The temporal resolution for matching. This should be a list made up of 'day', 'month', 'year'.
        Example, if you provide ['day', 'month', 'year'] model and observational data will be matched for each day of the year across all years.
        If you provide ['month', 'year'], the matches will occur by month, and days are ignored. In this case if the model resolution is daily,
        a monthly average will be calculated automatically.

    """

    #  loop through all time steps in the observational df....


    if self.temporal is False:
        # We need a quick hack
        df_times = []
        for ff in self.data:
            df_times.append(pd.DataFrame({"year":[None]}))
        df_times = pd.concat(df_times)
        self.data_times = df_times

        for x in ["year", "month", "day"]:
            if x in self.points.columns:
                self.points = self.points.drop(columns = x)
                print(f"Removing {x} from points dataframe")

    self.start_ag = self.data_ag
    self.ag_data = self.start_ag

    if on is None:
        on = "auto"

    if on != "auto":
        if type(on) is str:
            on = [on]

        if on == ["day"]:
             on = ["day", "month"]
        if type(on) is not list:
            raise ValueError("on must be a list")
        for x in on:
            if x not in ["day", "month", "year"]:
                raise ValueError(f"{x} is not a valid")

        _ag = on
        self.ag_data = on

        for x in ["day", "month", "year"]:
            if x not in on:
                if x in self.points.columns:
                    self.points = self.points.drop(columns=x)

    # This needs to work when there is no time
    if on == "auto":
        time_avail = [x for x in ["day", "month", "year"] if x in self.points.columns]
        if "day" in time_avail and "month" not in time_avail:
            time_avail.append("month")
        if len(time_avail) > 0:
            df_times = self.data_times.loc[:, self.data_ag].merge(
                self.points.loc[:, self.data_ag]
            )
            df_times = df_times.drop_duplicates()
            time_avail = [x for x in ["year", "month", "day"] if x in df_times.columns]
            if "day" in time_avail and "month" not in time_avail:
                time_avail.append("month")
            df_times = df_times.sort_values(by=time_avail).reset_index(drop=True)

            self.ag_data = time_avail

        else:
            df_times = None
    else:

        df_times = self.data_times.loc[:, on].merge(self.points.loc[:, on])
        df_times = df_times.drop_duplicates()
        time_avail = [x for x in ["year", "month", "day"] if x in df_times.columns]
        df_times = df_times.sort_values(by=time_avail).reset_index(drop=True)


    if self.temporal:
        if on == "auto":
            if "year" not in df_times.columns:
                if "year" in self.points.columns:
                    self.points = self.points.drop(columns="year")

            if "day" not in df_times.columns:
                self.points = self.points.drop(columns="day")
    else:
        df_times = self.data_times


    df_merged = []

    if self.temporal:
        self.ag_data.sort()

        if self.ag_data is not None:
            start_ag = self.start_ag
            ag_data = self.ag_data
            if "year" in ag_data:
                start_ag.append("year")
                start_ag = list(set(start_ag))
                start_ag.sort()
            ag_data.sort()
            if on == "auto":
                raise ValueError(f"Please specify the on arg. Suggested: {ag_data}")

            if ag_data != start_ag:

                if self.ag_data == ["day", "year"]:
                    print("Using a monthly climatology for model match ups")

                if self.ag_data == ["month", "year"]:
                    print("Using a multi-year monthly mean for model match ups")

                if self.ag_data == ["year"]:
                    print("Using a multi-year annual mean for model match ups")

                if self.ag_data == ["month"]:
                    print("Using a monthly climatology for model match ups")

                if self.ag_data == ["day", "month", "year"]:
                    print("Using a multi-year daily mean for model match ups")

        print(f"Temporal match up level: {self.ag_data}")

    n_matched = 0

    # depths only need to be calculated once
    if self.depths is not None:
        if type(self.depths) is not list:
            ds_depths = self.depths.copy()
            obs_locs = self.points.loc[:,["lon", "lat"]]
            ds_depths.regrid(obs_locs, "bil")
            if "deptht" in list(self.data.to_xarray().dims):
                df_depths = (
                    ds_depths.to_dataframe()
                    .reset_index()
                    .loc[:, ["lon", "lat", "depth"]]
                    .drop_duplicates()
                )
            else:
                df_depths = (
                    ds_depths.to_dataframe()
                    .reset_index()
                    .loc[:, ["lon", "lat"]]
                    .drop_duplicates()
                )
        else:
            df_depths = pd.DataFrame({"depth": self.depths})

        all_depths = df_depths


    for i in range(0, len(df_times)):
        if self.temporal:
            i_df = df_times.iloc[
                i : (i + 1) :,
            ]
            i_grid = self.points.merge(i_df).loc[:, ["lon", "lat"]]
            if "year" in self.points.columns:
                i_year = i_df.year.values[0]
            if "month" in self.points.columns:
                i_month = i_df.month.values[0]
            if "day" in self.points.columns:
                i_day = i_df.day.values[0]

            ds = open_data(set(self.data_times.merge(i_df).path), checks=False)
        else:
            ds = open_data(self.data, checks=False)
            i_grid = self.points.loc[:, ["lon", "lat"]].drop_duplicates()


        if self.variables is not None:
            ds.select(variables=self.variables)

        if self.temporal:
            for opt in ["day", "year", "month"]:
                if "day" in self.points.columns:
                    ds.select(day=i_day)
                if "month" in self.points.columns:
                    ds.select(month=i_month)
                if "year" in self.points.columns:
                    ds.select(year=i_year)

                ds.tmean(self.ag_data)

        if self.data_nan is not None:
            ds.set_missing(self.data_nan)

        ds.regrid(i_grid, "bil")

        df_model = ds.to_dataframe().drop_duplicates().reset_index().drop_duplicates()

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
                df_model = df_model.loc[ :, locs ].drop_duplicates()


            i_obs_df = i_df.merge(self.points)
            i_obs_locs = i_obs_df.loc[:, ["lon", "lat"]].drop_duplicates()

            if True:

                for j in range(0, len(i_obs_locs)):
                    if self.depths is not None:
                        df_depths = all_depths.merge(i_obs_locs)

                    j_obs = i_obs_locs.iloc[j : (j + 1), :].merge(i_obs_df)

                    j_model = (
                        df_model.merge(j_obs.loc[:, ["lon", "lat"]])
                        .drop_duplicates()
                        .reset_index(drop=True)
                    )

                    if len(j_model) > 0:
                        if type(self.depths) is not list:
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
                                locs = ["lon", "lon", "depth"]
                                locs += ds.variables
                                j_model = j_model.merge(
                                    df_depths, left_index=True, right_index=True
                                ).loc[:, locs]
                        if self.depths is not None:
                            max_depth = np.max(j_model.depth)
                            min_depth = np.min(j_model.depth)
                            j_obs = (
                                j_obs.query("depth <= @max_depth")
                                .query("depth >= @min_depth")
                                .reset_index(drop=True)
                            )
                        if len(j_obs) > 0:

                            if self.depths is not None:
                                i_var = 0
                                for var in ds.variables:
                                    f = scipy.interpolate.interp1d(
                                        j_model.depth, j_model[var]
                                    )
                                    j_obs[var] = f(j_obs.depth)

                                    i_var +=1
                                df_merged.append(j_obs)
                            else:
                                df_merged.append(j_model)

    if len(df_merged) == 0:
        raise ValueError("No data matches were found")

    df_merged = pd.concat(df_merged).drop_duplicates().reset_index(drop=True)
    if len([x for x in df_merged.columns if x.startswith("time")]) == 1:
        try:
            time_name = [x for x in df_merged.columns if x.startswith("time")][0]
            times = df_merged[time_name]
            df_merged["year"] = [x.year for x in times]
            df_merged["month"] = [x.month for x in times]
            df_merged["day"] = [x.day for x in times]
            df_merged = df_merged.drop(columns = time_name)
        except:
            df_merged = df_merged




    self.matched = df_merged
