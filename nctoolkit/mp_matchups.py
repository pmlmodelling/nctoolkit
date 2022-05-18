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


    self.start_ag = self.model_ag
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

        self.model_ag = on
        self.ag_data = on

        for x in ["day", "month", "year"]:
            if x not in on:
                if x in self.obs.columns:
                    self.obs = self.obs.drop(columns=x)

    # This needs to work when there is no time
    if on == "auto":
        time_avail = [x for x in ["day", "month", "year"] if x in self.obs.columns]
        if "day" in time_avail and "month" not in time_avail:
            time_avail.append("month")
        if len(time_avail) > 0:
            df_times = self.model_times.loc[:, self.model_ag].merge(
                self.obs.loc[:, self.model_ag]
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

        df_times = self.model_times.loc[:, on].merge(self.obs.loc[:, on])
        df_times = df_times.drop_duplicates()
        time_avail = [x for x in ["year", "month", "day"] if x in df_times.columns]
        df_times = df_times.sort_values(by=time_avail).reset_index(drop=True)

        # df_times = self.obs.loc[:, time_avail].drop_duplicates()

    if on == "auto":
        if "year" not in df_times.columns:
            if "year" in self.obs.columns:
                self.obs = self.obs.drop(columns="year")

        if "day" not in df_times.columns:
            self.obs = self.obs.drop(columns="day")


    df_merged = []

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

    if True:
        for i in range(0, len(df_times)):
            i_df = df_times.iloc[
                i : (i + 1) :,
            ]
            i_grid = self.obs.merge(i_df).loc[:, ["lon", "lat"]]
            if "year" in self.obs.columns:
                i_year = i_df.year.values[0]
            if "month" in self.obs.columns:
                i_month = i_df.month.values[0]
            if "day" in self.obs.columns:
                i_day = i_df.day.values[0]

            ds = open_data(set(self.model_times.merge(i_df).path), checks=False)

            target = list(self.model_map.values())[0]

            variable = self.variable
            if is_equation(target):
                ds.cdo_command(f"expr,'{variable}=target'")
            else:
                ds.select(variables=target)

            for opt in ["day", "year", "month"]:
                if "day" in self.obs.columns:
                    ds.select(day=i_day)
                if "month" in self.obs.columns:
                    ds.select(month=i_month)
                if "year" in self.obs.columns:
                    ds.select(year=i_year)

                ds.tmean(self.ag_data)

            if self.model_nan is not None:
                ds.set_missing(self.model_nan)
            if self.top:
                ds.regrid(i_grid, "nn")
            else:
                ds.regrid(i_grid, "nn")
            ds.rename({ds.variables[0]: variable})

            df_model = ds.to_dataframe().reset_index()

            # figure out the time dim

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

            if self.top:
                df_model = df_model.loc[
                    :, [time_name, "lon", "lat", variable]
                ].drop_duplicates()
                i_obs_df = i_df.merge(self.obs)
                df_merged.append(
                    i_obs_df.rename(columns={variable: "observation"}).merge(
                        df_model.rename(columns={variable: "model"})
                    )
                )

            else:

                if "deptht" in df_model.columns:
                    df_model = df_model.loc[
                        :, [time_name, "lon", "lat", "deptht", variable]
                    ].drop_duplicates()
                else:
                    df_model = df_model.loc[
                        :, [time_name, "lon", "lat", variable]
                    ].drop_duplicates()

                if self.top is False:
                    if type(self.depths) is not list:
                        ds_depths = self.depths.copy()

                i_obs_df = i_df.merge(self.obs)
                i_obs_locs = i_obs_df.loc[:, ["lon", "lat"]].drop_duplicates()

                if self.top:
                    df_model = self.model.to_dataframe().reset_index()

                else:
                    if type(self.depths) is not list:
                        ds_depths.regrid(i_obs_locs, "nn")
                        if "deptht" in df_model.columns:
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

                    for j in range(0, len(i_obs_locs)):
                        j_obs = i_obs_locs.iloc[j : (j + 1), :].merge(i_obs_df)
                        j_model = (
                            df_model.merge(j_obs.loc[:, ["lon", "lat"]])
                            .drop_duplicates()
                            .reset_index(drop=True)
                        )

                        if len(j_model) > 0:
                            if type(self.depths) is not list:
                                j_depths = (
                                    df_depths.merge(j_obs.loc[:, ["lon", "lat"]])
                                    .drop_duplicates()
                                    .reset_index(drop=True)
                                )
                                j_model = j_model.merge(
                                    j_depths, left_index=True, right_index=True
                                ).loc[:, ["lon_x", "lon_y", "depth", self.variable]]
                            else:
                                j_model = j_model.merge(
                                    df_depths, left_index=True, right_index=True
                                ).loc[:, ["lon", "lon", "depth", self.variable]]
                            max_depth = np.max(j_model.depth)
                            min_depth = np.min(j_model.depth)
                            j_obs = (
                                j_obs.query("depth < @max_depth")
                                .query("depth > @min_depth")
                                .reset_index(drop=True)
                            )
                            if len(j_obs) > 0:

                                f = scipy.interpolate.interp1d(
                                    j_model.depth, j_model[self.variable]
                                )
                                j_obs[f"model"] = f(j_obs.depth)
                                j_obs = j_obs.rename(
                                    columns={self.variable: "observation"}
                                ).assign(variable=self.variable)
                                df_merged.append(j_obs)

    df_merged = pd.concat(df_merged).drop_duplicates().reset_index(drop=True)

    self.matched = df_merged
