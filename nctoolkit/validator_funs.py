import pandas as pd

from nctoolkit.unify import unify
from nctoolkit.api import open_data
from nctoolkit.api import cor_time
from nctoolkit.api import cor_space


class Validation(object):
    """
    A model validation object
    """

    def __init__(self, start=""):
        """Initialize the starting file name etc"""
        # Attribuates of interest to users
        self.data = None
        #self.plot = None
        self.plot_type = None
        self.info = None
    def __repr__(self):
        return f"Validation object: {self.info}"

    @property
    def plot(self):
        if self.plot_type == "nctoolkit":
            return self.data.plot(title = self.info)
        else:
            return self._ggplot

def get_type(ds):
    times = ds.times

    df = pd.DataFrame(
        {
            "year": [x.year for x in times],
            "month": [x.month for x in times],
            "day": [x.day for x in times],
        }
    )
    if df.groupby(["year", "month"]).size().max() > 1:
        if len(df.loc[:, ["year"]].drop_duplicates()) > 1:
            return ["year", "month", "day"]
        else:
            return ["day"]

    if len(df.loc[:, ["year"]].drop_duplicates()) == len(df):
        return ["year"]

    if len(df.loc[:, ["month"]].drop_duplicates()) == len(df):
        return ["month"]

    if len(df.loc[:, ["year", "month"]].drop_duplicates()) == len(df):
        return ["year", "month"]




def add_model(self, ds = None, map = None, nan = None , precision = None, **kwargs):
    """
    Add model data

    Parameters
    -------------
    ds: Dataset

    map: dict
        Dictionary mapping model variables to validation variables

    nan: float or list
        Value or range of values to set to nan. Defaults to None, o no changes to missing values.
    precision: numerical precision if needed
        Choose "F64" if advised by a warning

    """

    if self.model is not None:
        raise ValueError("You have already added model data!")

    if not isinstance(map, dict):
        raise ValueError("You must provided a map")

    if len(map) != 1:
        raise ValueError("There should only be one variable in the map!")


    self.model = ds.copy()
    self.model_map = map
    self.model_nan = nan
    self.model_precision = precision

    for kk in kwargs:
        if kk == "amm7":
            if kwargs[kk]:
                self.model.amm7 = True


def add_observations(self, ds = None, map = None, nan = None , precision = None):
    """
    Add observational data

    Parameters
    -------------
    ds: Dataset
    map: dict
        Dictionary mapping observational variables to validation variables

    nan: float or list
        Value or range of values to set to nan
    precision: numerical precision if needed
        Choose "F64" if advised by a warning

    """

    if not isinstance(map, dict):
        raise ValueError("You must provided a map")

    if len(map) != 1:
        raise ValueError("There should only be one variable in the map!")

    if self.obs is not None:
        raise ValueError("You have already added observation data!")
    self.obs = ds.copy()

    self.obs_map = map
    self.obs_nan = nan
    self.obs_precision = precision



import re


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_equation(x):
    regexp = re.compile(r"[+,\-,/, \* ]")
    return len(regexp.findall(x)) > 0

def matchup(self, levels = "top", na_match = False, **kwargs):

    expected_model_vars = []
    for key, value in self.model_map.items():
        expected_model_vars += re.findall(r"\w+", value)

    expected_obs_vars = []
    for key, value in self.obs_map.items():
        expected_obs_vars += re.findall(r"\w+", value)

    model_vars = self.model.variables
    obs_vars = self.obs.variables

    for vv in expected_model_vars:
        if is_number(vv) is False:
            if vv not in model_vars:
                raise ValueError(f"{vv} does not exist in model data!. Available vars: {model_vars}")

    for vv in expected_obs_vars:
        if is_number(vv) is False:
            if vv not in obs_vars:
                raise ValueError(f"{vv} does not exist in observational data! Available vars: {obs_vars}")


    if self.model_map is None or self.model_map is None:
        raise ValueError("You must provide maps for model and observational data!")

    if set(self.model_map.keys()) != set(self.obs_map.keys()):
        raise ValueError("Variables in maps should match")

    # Step 1. Figure out the levels


   # extract some variables....

    keep_these = []
    for key, value in self.model_map.items():
        keep_these += re.findall(r"\w+", value)

    self.model.subset(variables=keep_these)

    # Only select the top level

    if levels == "top":
        self.model.top()
        self.obs.top()

    if len(self.model) > 1:
        self.model.merge("time")

    if len(self.obs) > 1:
        self.obs.merge("time")


    self.model.run()

    if self.model_nan is not None:
        print("Fixing missing values in model data!")
        self.model.as_missing(self.model_nan)
    if self.obs_nan is not None:
        print("Fixing missing values in observation data!")
        self.model.as_missing(self.obs_nan)

    for key, value in self.model_map.items():
        if is_equation(value) is False:
            self.model.rename({value: key})
        else:
            fixed_value = value.replace("(", "\(")
            fixed_value = fixed_value.replace(")", "\)")
            self.model.cdo_command(f"aexpr,{key}={fixed_value}")

    keep_these = []
    for key, value in self.obs_map.items():
        keep_these += re.findall(r"\w+", value)

    self.obs.subset(variables=keep_these)

    for key, value in self.obs_map.items():
        if is_equation(value) is False:
            self.obs.rename({value: key})
        else:
            fixed_value = value.replace("(", "\(")
            fixed_value = fixed_value.replace(")", "\)")
            self.obs.cdo_command(f"aexpr,'{key}={fixed_value}'")

    self.model.subset(variables=list(self.model_map.keys()))
    self.obs.subset(variables=list(self.obs_map.keys()))


    try:
        self.model.amm7
        unify(self.model, self.obs, amm7 = True)
    except:
        unify(self.model, self.obs)

    self.aggregation = get_type(self.model)


    if na_match:
        print("Matching missing values in model and observation datasets")

        mask = self.model.copy()
        mask.rename({list(self.model_map.keys())[0]: "variable"})
        mask.assign(variable = lambda x: isnan(x.variable) == False)
        mask.as_missing(0)

        self.model.multiply(mask)
        self.obs.multiply(mask)

        mask = self.obs.copy()
        mask.rename({list(self.model_map.keys())[0]: "variable"})
        mask.assign(variable = lambda x: isnan(x.variable) == False)
        mask.as_missing(0)

        self.model.multiply(mask)
        self.obs.multiply(mask)

        self.model.run()
        self.obs.run()


    self.matched = True







def validate(self, region = None):

    try:
        from plotnine import ggplot
    except:
        raise ValueError("Please install plotnine")

    if self.matched is False:
        raise ValueError("Data has not been matched")

    self.results  = []

    if "month" in self.aggregation or "day" in self.aggregation:
        val = Validation()
        ds_model = self.model.copy()
        ds_obs = self.obs.copy()

        if len(self.model.years) > 1:
            ds_model.tmean("month")
            ds_obs.tmean("month")
        model_vars = ds_model.variables[0]

        ds_cor = cor_time(ds_model, ds_obs)

        val.data = ds_cor.copy()
        val.info = f"Temporal correlation coefficient between monthly climatological {model_vars} in model and observation"

        val.plot_type = "nctoolkit"

        self.results.append(val)

    ## Annual bias

    if len(self.model.months) == 12:

        val = Validation()

        ds_val = open_data()
        ds_model = self.model.copy()
        ds_obs = self.obs.copy()
        ds_model.tmean(["year", "month"])
        ds_obs.tmean(["year", "month"])
        ds_model.tmean(["year"])
        ds_obs.tmean(["year"])
        ds_model.subtract(ds_obs)
        ds_model.tmean()
        ds_model.rename({self.model.variables[0]: "absolute"})
        ds_val.append(ds_model)


        ds_model = self.model.copy()
        ds_obs = self.obs.copy()
        ds_model.tmean(["year", "month"])
        ds_obs.tmean(["year", "month"])
        ds_model.tmean(["year"])
        ds_obs.tmean(["year"])
        ds_model.tmean()
        ds_model.divide(ds_obs)
        ds_model.subtract(1)
        ds_model.multiply(100)
        ds_model.rename({self.model.variables[0]: "relative"})
        ds_model.set_longnames({ "relative":"Percentage difference"})
        ds_model.set_units({ "relative":"%"})
        ds_val.append(ds_model)
        ds_val.merge("variable")

        val.info= "Annual climatological bias (model -/ observation)"
        val.plot_type = "nctoolkit"
        val.data = ds_val.copy()
        self.results.append(val)


    if "month" in self.aggregation or "day" in self.aggregation:
        # Try to find the units
        if region is None:

            ds_model = self.model.copy()

            model_vars = ds_model.variables

            model_units = dict()
            for vv in model_vars:
                try:
                    vv_unit = ds_model.contents.query("variable = @vv").unit.values[0]
                    if vv_unit is not None:
                        model_units[vv] = vv_unit
                except:
                    whatever = None

            for vv in model_vars:
                try:
                    vv_unit = ds_obs.contents.query("variable = @vv").unit.values[0]
                    if vv_unit is not None:
                        model_units[vv] = vv_unit
                except:
                    whatever = None

            model_time = [
                x for x in self.model.to_xarray().dims if x.startswith("time")
            ][0]

            sel = [model_time]
            sel += model_vars

            all_df = []

            rr_model = ds_model.copy()
            rr_model.tmean("month")
            rr_model.spatial_mean()
            rr_df = (
                rr_model.to_dataframe()
                .reset_index()
                .loc[:, sel]
                .assign(source="Model")
                .rename(columns={model_time: "time"})
                .assign(month=lambda x: x.time.dt.month)
                .drop(columns="time")
                .drop_duplicates()
            )

            all_df.append(rr_df)

            ds_obs = self.obs.copy()

            obs_vars = ds_obs.variables

            obs_time = [x for x in self.obs.to_xarray().dims if x.startswith("time")][0]

            sel = [obs_time]
            sel += obs_vars

            rr_obs = ds_obs.copy()
            rr_obs.tmean("month")
            rr_obs.spatial_mean()
            rr_df = (
                rr_obs.to_dataframe()
                .reset_index()
                .loc[:, sel]
                .assign(source="Observation")
                .rename(columns={obs_time: "time"})
                .assign(month=lambda x: x.time.dt.month)
                .drop(columns="time")
                .drop_duplicates()
            )
            all_df.append(rr_df)

            all_df = pd.concat(all_df)

            id_vars = [x for x in all_df.columns if x not in model_vars]

            all_df = all_df.melt(value_vars=model_vars, id_vars=id_vars)

            ylab = model_vars[0]

            val = Validation()

            val.info = f"Monthly climatologies of model and observational data for {ylab}"

            if ylab in model_units.keys():
                ylab = ylab + "(" + model_units[ylab] + ")"

            plot = (
                ggplot(all_df.dropna())
                + geom_line(aes("month", "value", colour="source"))
                + labs(y=ylab)
                + labs(title=val.info)
            )

            val._ggplot = plot
            val.data = all_df
            self.results.append(val)


        if region is not None:

            regions = region.copy()

            ds_model = self.model.copy()

            model_vars = ds_model.variables

            model_units = dict()
            for vv in model_vars:
                try:
                    vv_unit = ds_model.contents.query("variable = @vv").unit.values[0]
                    if vv_unit is not None:
                        model_units[vv] = vv_unit
                except:
                    whatever = None

            for vv in model_vars:
                try:
                    vv_unit = ds_obs.contents.query("variable = @vv").unit.values[0]
                    if vv_unit is not None:
                        model_units[vv] = vv_unit
                except:
                    whatever = None

            model_time = [
                x for x in self.model.to_xarray().dims if x.startswith("time")
            ][0]

            sel = [model_time]
            sel += model_vars

            all_df = []

            for rr in regions.variables:
                rr_ds = regions.copy()
                rr_ds.subset(variable=rr)
                rr_model = ds_model.copy()
                rr_model.multiply(rr_ds)
                rr_model.tmean("month")
                rr_model.spatial_mean()
                rr_df = (
                    rr_model.to_dataframe()
                    .reset_index()
                    .loc[:, sel]
                    .assign(source="Model")
                    .rename(columns={model_time: "time"})
                    .assign(month=lambda x: x.time.dt.month)
                    .assign(region=rr)
                    .drop(columns="time")
                )
                all_df.append(rr_df)

            ds_obs = self.obs.copy()

            obs_vars = ds_obs.variables

            obs_time = [x for x in self.obs.to_xarray().dims if x.startswith("time")][0]

            sel = [obs_time]
            sel += obs_vars

            for rr in regions.variables:
                rr_ds = regions.copy()
                rr_ds.subset(variable=rr)
                rr_obs = ds_obs.copy()
                rr_obs.multiply(rr_ds)
                rr_obs.tmean("month")
                rr_obs.spatial_mean()
                rr_df = (
                    rr_obs.to_dataframe()
                    .reset_index()
                    .loc[:, sel]
                    .assign(source="Observation")
                    .rename(columns={obs_time: "time"})
                    .assign(month=lambda x: x.time.dt.month)
                    .assign(region=rr)
                    .drop(columns="time")
                )
                all_df.append(rr_df)

            all_df = pd.concat(all_df)

            id_vars = [x for x in all_df.columns if x not in model_vars]

            all_df = all_df.melt(value_vars=model_vars, id_vars=id_vars)

            ylab = model_vars[0]
            val = Validation()

            val.info =  f"Monthly climatologies of model and observational data for {ylab}"

            if ylab in model_units.keys():
                ylab = ylab + "(" + model_units[ylab] + ")"

            plot = (
                ggplot(all_df.dropna())
                + geom_line(aes("month", "value", colour="source"))
                + facet_wrap("region")
                + labs(y=ylab)
                + labs(title=val.info)
            )
            val._ggplot = plot
            val.plot_type = "plotnine"

            self.results.append(val)

        # Monthly biases plot
        val = Validation()

        val.info = "Monthly climatological bias (model - observation)"

        ds_bias = self.model.copy()
        ds_bias.subtract(self.obs)
        ds_bias.tmean("month")

        val.data = ds_bias.copy()

        val.plot_type  = "nctoolkit"
        self.results.append(val)

    # Plot the annual time series...
    if "year" in self.aggregation and len(self.model.years) > 1:
        # Try to find the units

        if region is not None:
            regions = nc.open_data(stream)

            ds_model = self.model.copy()

            model_vars = ds_model.variables

            model_units = dict()
            for vv in model_vars:
                try:
                    vv_unit = ds_model.contents.query("variable = @vv").unit.values[0]
                    if vv_unit is not None:
                        model_units[vv] = vv_unit
                except:
                    whatever = None

            for vv in model_vars:
                try:
                    vv_unit = ds_obs.contents.query("variable = @vv").unit.values[0]
                    if vv_unit is not None:
                        model_units[vv] = vv_unit
                except:
                    whatever = None

            model_time = [
                x for x in self.model.to_xarray().dims if x.startswith("time")
            ][0]

            sel = [model_time]
            sel += model_vars

            all_df = []

            for rr in regions.variables:
                rr_ds = regions.copy()
                rr_ds.subset(variable=rr)
                rr_model = ds_model.copy()
                rr_model.multiply(rr_ds)
                rr_model.tmean(["year", "month"])
                rr_model.tmean("year")
                rr_model.spatial_mean()
                rr_df = (
                    rr_model.to_dataframe()
                    .reset_index()
                    .loc[:, sel]
                    .assign(source="Model")
                    .rename(columns={model_time: "time"})
                    .assign(year=lambda x: x.time.dt.year)
                    .assign(region=rr)
                    .drop(columns="time")
                )
                all_df.append(rr_df)

            ds_obs = self.obs.copy()

            obs_vars = ds_obs.variables

            obs_time = [x for x in self.obs.to_xarray().dims if x.startswith("time")][0]

            sel = [obs_time]
            sel += obs_vars

            for rr in regions.variables:
                rr_ds = regions.copy()
                rr_ds.subset(variable=rr)
                rr_obs = ds_obs.copy()
                rr_obs.multiply(rr_ds)
                rr_obs.tmean(["year", "month"])
                rr_obs.tmean("year")
                rr_obs.spatial_mean()
                rr_df = (
                    rr_obs.to_dataframe()
                    .reset_index()
                    .loc[:, sel]
                    .assign(source="Observation")
                    .rename(columns={obs_time: "time"})
                    .assign(year=lambda x: x.time.dt.year)
                    .assign(region=rr)
                    .drop(columns="time")
                )
                all_df.append(rr_df)

            all_df = pd.concat(all_df)

            id_vars = [x for x in all_df.columns if x not in model_vars]

            all_df = all_df.melt(value_vars=model_vars, id_vars=id_vars)

            ylab = model_vars[0]

            val = Validation()
            val.info =  f"Annual means of model and observational data for {ylab}"

            if ylab in model_units.keys():
                ylab = ylab + "(" + model_units[ylab] + ")"

            plot = (
                ggplot(all_df)
                + geom_line(aes("year", "value", colour="source"))
                + facet_wrap("region")
                + labs(y=ylab)
                + labs(title=val.info)
            )
            val._ggplot = plot
            val.plot_type = "plotnine"

            self.results.append(val)

        if region is None:

            ds_model = self.model.copy()

            model_vars = ds_model.variables

            model_units = dict()
            for vv in model_vars:
                try:
                    vv_unit = ds_model.contents.query("variable = @vv").unit.values[0]
                    if vv_unit is not None:
                        model_units[vv] = vv_unit
                except:
                    whatever = None

            for vv in model_vars:
                try:
                    vv_unit = ds_obs.contents.query("variable = @vv").unit.values[0]
                    if vv_unit is not None:
                        model_units[vv] = vv_unit
                except:
                    whatever = None

            model_time = [
                x for x in self.model.to_xarray().dims if x.startswith("time")
            ][0]

            sel = [model_time]
            sel += model_vars

            all_df = []

            rr_model = ds_model.copy()
            rr_model.tmean(["year", "month"])
            rr_model.tmean("year")
            rr_model.spatial_mean()
            rr_df = (
                rr_model.to_dataframe()
                .reset_index()
                .loc[:, sel]
                .assign(source="Model")
                .rename(columns={model_time: "time"})
                .assign(year=lambda x: x.time.dt.year)
                .drop(columns="time")
            )
            all_df.append(rr_df)

            ds_obs = self.obs.copy()

            obs_vars = ds_obs.variables

            obs_time = [x for x in self.obs.to_xarray().dims if x.startswith("time")][0]

            sel = [obs_time]
            sel += obs_vars

            rr_obs = ds_obs.copy()
            rr_obs.tmean(["year", "month"])
            rr_obs.tmean("year")
            rr_obs.spatial_mean()
            rr_df = (
                rr_obs.to_dataframe()
                .reset_index()
                .loc[:, sel]
                .assign(source="Observation")
                .rename(columns={obs_time: "time"})
                .assign(year=lambda x: x.time.dt.year)
                .drop(columns="time")
            )
            all_df.append(rr_df)

            all_df = pd.concat(all_df)

            id_vars = [x for x in all_df.columns if x not in model_vars]

            all_df = all_df.melt(value_vars=model_vars, id_vars=id_vars)

            ylab = model_vars[0]

            val = Validation()
            val.info = f"Annual means of model and observational data for {ylab}"

            if ylab in model_units.keys():
                ylab = ylab + "(" + model_units[ylab] + ")"

            plot = (
                ggplot(all_df)
                + geom_line(aes("year", "value", colour="source"))
                + labs(y=ylab)
                + labs(title=val.info)
            )

            val._ggplot = plot
            val.data = all_df
            self.results.append(val)



