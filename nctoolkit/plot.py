import sys

from netCDF4 import Dataset
from threading import Thread

import time
import subprocess
import holoviews as hv
#import matplotlib
import panel as pn
import pandas as pd
import hvplot.pandas
import hvplot.xarray
from bokeh.plotting import show
import xarray as xr
import cftime
from nctoolkit.api import open_data
import warnings

from nctoolkit.utils import is_curvilinear

hv.extension("bokeh")
hv.Store.renderers


def variable_dims(ff):
    """
    Levels and points for variables in a dataset
    """

    cdo_result = subprocess.run(
        "cdo showname " + ff,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    cdo_result = (
        str(cdo_result.stdout)
        .replace("b'", "")
        .replace("\\n", "")
        .replace("'", "")
        .strip()
    )
    cdo_result = cdo_result.split()

    out = subprocess.run(
        "cdo sinfon " + ff,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out = out.stdout.decode("utf-8")
    out = out.split("\n")
    out_inc = ["Grid coordinates :" in ff for ff in out]
    var_det = []
    i = 1
    while True:
        if out_inc[i]:
            break
        i += 1
        var_det.append(out[i - 1])

    var_det = [ff.replace(":", "") for ff in var_det]
    var_det = [" ".join(ff.split()) for ff in var_det]
    var_det = [ff.replace("Parameter name", "variable").split(" ") for ff in var_det]
    sales = var_det[1:]
    labels = var_det[0]
    df = pd.DataFrame.from_records(sales, columns=labels)
    df = df.assign(Points=lambda x: x.Points.astype("int"))
    return df


def ctrc():
    time.sleep(1)
    print("Press Ctrl+C to stop plotting server")



def in_notebook():
    """
    Returns ``True`` if the module is running in IPython kernel,
    ``False`` if in IPython shell or other Python shell.
    """
    return "ipykernel" in sys.modules


def plot(self, vars=None, log=False, panel=False):

    """
    Autoplotting method.
    Automatically plot a dataset.

    Parameters
    -------------
    log: boolean
        Do you want a plotted data to be logged?
    vars: str or list
        A string or list of the variables to plot
    panel: boolean
        Do you want a panel plot, if avaiable?
    """

    if type(log) is not bool:
        raise TypeError("log is not boolean")

    if type(panel) is not bool:
        raise TypeError("panel is not boolean")

    self.run()

    if type(self.current) is list:
        raise TypeError("You cannot view multiple files!")

    cdo_result = subprocess.run(
        "cdo ngrids " + self.current,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    cdo_result = subprocess.run(
        "cdo nlevel " + self.current,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    n_levels = variable_dims(self.current).Levels.astype("int").max()

    cdo_result = subprocess.run(
        "cdo ntime " + self.current,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    n_times = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    cdo_result = subprocess.run(
        "cdo ngridpoints " + self.current,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    n_points = variable_dims(self.current).Points.astype("int").max()

    if vars is None and n_points > 1:
        vars = list(variable_dims(self.current).query("Points>1").variable)

    if vars is None and n_points == 1:
        vars = self.variables

    if type(vars) is list:
        if len(vars) == 1:
            vars = vars[0]


    # Case when all you can plot is a time series

    out = subprocess.run(
        "cdo griddes " + self.current,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    lon_name = [
        x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x
    ][-1].split(" ")[-1]
    lat_name = [
        x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x
    ][-1].split(" ")[-1]

    # heat map 1
    data = open_data(self.current)
    ds = data.to_xarray()


    coord_list = list(ds.coords)
    coord_df = pd.DataFrame({"coord":coord_list, "length":[len(ds.coords[x].values) for x in coord_list]})


    # line plot
    if len([x for x in coord_df.length if x > 1]) == 1:

        df = (
                ds
                .to_dataframe()
                .reset_index()
                )
        x_var = coord_df.query("length > 1").reset_index().coord[0]

        if type(vars) is str:
            vars = [vars]

        selection = [x for x in df.columns if x in vars or x == x_var]
        df = (
                df
                .loc[:, selection]
                .melt(x_var)
                .drop_duplicates()
                .set_index(x_var)
                )

        if panel:
            intplot = (
                df
                .hvplot(
                    by="variable",
                    logy=log,
                    subplots=True,
                    shared_axes=False,
                    responsive=(in_notebook() is False),
                )
            )
            if in_notebook():
                return intplot

            t = Thread(target=ctrc)
            t.start()

            bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
                threaded=False
            )
            return None
        else:
            intplot = (
                df
                .hvplot(
                    groupby="variable",
                    logy=log,
                    dynamic=True,
                    responsive=(in_notebook() is False),
                )
            )
            if in_notebook():
                return intplot

            t = Thread(target=ctrc)
            t.start()

            bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
                threaded=False
            )
            return None


    # heat map where 2 coords have more than 1 value, not a spatial map
    if len([x for x in coord_df.length if x > 1]) == 2:

        df = (
                ds
                .to_dataframe()
                .reset_index()
                )
        x_var = coord_df.query("length > 1").reset_index().coord[0]
        y_var = coord_df.query("length > 1").reset_index().coord[1]

        selection = [x for x in df.columns if x in vars or x == x_var or x == y_var]

        df = (
                df
                .loc[:, selection]
                .melt([x_var, y_var])
                .drop_duplicates()
                )
        if (len(ds.coords[lon_name].values) ==1) or (len(ds.coords[lat_name].values) == 1):

            intplot = df.drop_duplicates().hvplot.heatmap(x=x_var, y=y_var, C= "value", groupby = "variable",  colorbar=True)
            if in_notebook():
                return intplot

            t = Thread(target=ctrc)
            t.start()
            bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
                    threaded=False
                )
            return None


    # heat map where 3 coords have more than 1 value, and one of them is time. Not a spatial map though
    if len([x for x in coord_df.length if x > 1]) == 3:

        time_in = False

        possible = 0
        for x in coord_list:
            if "time" in x:
                time_in = True
                possible += 1

        if possible > 1:
            time_in = False


        if "time" in coord_list and time_in:

            if coord_df.query("coord == 'time'").length.values > 1:

                df = (
                        ds
                        .to_dataframe()
                        .reset_index()
                        )
                x_var = coord_df.query("length > 1").query("coord != 'time'").reset_index().coord[0]
                y_var = coord_df.query("length > 1").query("coord != 'time'").reset_index().coord[1]

                selection = [x for x in df.columns if x in vars or x == x_var or x == y_var or x == "time"]

                df = (
                        df
                        .loc[:, selection]
                        .melt([x_var, y_var, "time"])
                        .drop_duplicates()
                        )
                if (len(ds.coords[lon_name].values) ==1) or (len(ds.coords[lat_name].values) == 1):

                    intplot = df.drop_duplicates().hvplot.heatmap(x=x_var, y=y_var, C= "value", groupby = ["variable", "time"],  colorbar=True)
                    if in_notebook():
                        return intplot

                    t = Thread(target=ctrc)
                    t.start()
                    bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
                            threaded=False
                        )
                    return None




    #if ((len(self.to_xarray()[lon_name]) == 1) or (len(self.to_xarray()[lat_name])==1)) and n_levels < 2:
    #    if (len(self.to_xarray()[lon_name]) > 1) or (len(self.to_xarray()[lat_name]) > 1):
    #        if len(self.variables) == 1 and len(self.times) > 1:

    #            if len(self.to_xarray()[lon_name]) == 1:
    #                df =  self.to_dataframe().reset_index().loc[:,["time", self.variables[0], lat_name]]
    #                intplot =  df.drop_duplicates().hvplot.heatmap(x=lat_name, y='time', C=self.variables[0], colorbar=True)

    #            if len(self.to_xarray()[lat_name]) == 1:
    #                df =  self.to_dataframe().reset_index().loc[:,["time", self.variables[0], lon_name]]
    #                intplot =  df.drop_duplicates().hvplot.heatmap(x=lon_name, y='time', C=self.variables[0], colorbar=True)


    #            if in_notebook():
    #                return intplot

    #            t = Thread(target=ctrc)
    #            t.start()
    #            bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
    #                    threaded=False
    #                )
    #            return None




    #        if len(self.variables) >= 1 and len(self.times) == 1:
    #            #if len(self.to_xarray()[lon_name]) == 1:
    #            #    df =  self.to_dataframe().reset_index().loc[:,["time", self.variables[0], lat_name]]
    #            #    return df.drop_duplicates().hvplot(x=lat_name, y=self.variables[0])

    #            #if len(self.to_xarray()[lat_name]) == 1:
    #            #    df =  self.to_dataframe().reset_index().loc[:,["time", self.variables[0], lon_name]]
    #            #    return df.drop_duplicates().hvplot(x=lon_name, y=self.variables[0])
    #            vars = self.variables
    #            if type(vars) is str:
    #                vars = [vars]

    #            df = self.to_xarray()

    #            dim_dict = dict(df.dims)
    #            to_go = []
    #            for kk in dim_dict.keys():
    #                if dim_dict[kk] == 1:
    #                    df = df.squeeze(kk)
    #                    to_go.append(kk)

    #            df = df.to_dataframe()
    #            keep = self.variables
    #            df = df.reset_index()

    #            if len(self.to_xarray()[lat_name]) == 1:
    #                to_go = [x for x in df.columns if (x not in [lon_name] and x not in keep)]
    #                x_var = lon_name
    #                df = (
    #                        df.drop(columns=to_go)
    #                        .drop_duplicates()
    #                        .set_index(x_var)
    #                        .loc[:, vars]
    #                        .reset_index()
    #                        .melt(lon_name)
    #                        .set_index(x_var)
    #                        )
    #            else:
    #                to_go = [x for x in df.columns if (x not in [lat_name] and x not in keep)]
    #                x_var = lat_name
    #                df = (
    #                        df.drop(columns=to_go)
    #                        .drop_duplicates()
    #                        .set_index(x_var)
    #                        .loc[:, vars]
    #                        .reset_index()
    #                        .melt(lat_name)
    #                        .set_index(x_var)
    #                        )

    #            if panel:
    #                intplot = (
    #                    df
    #                    .hvplot(
    #                        by="variable",
    #                        logy=log,
    #                        subplots=True,
    #                        shared_axes=False,
    #                        responsive=(in_notebook() is False),
    #                    )
    #                )
    #                if in_notebook():
    #                    return intplot

    #                t = Thread(target=ctrc)
    #                t.start()

    #                bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
    #                    threaded=False
    #                )
    #                return None
    #            else:
    #                intplot = (
    #                    df
    #                    .hvplot(
    #                        groupby="variable",
    #                        logy=log,
    #                        dynamic=True,
    #                        responsive=(in_notebook() is False),
    #                    )
    #                )
    #                if in_notebook():
    #                    return intplot

    #                t = Thread(target=ctrc)
    #                t.start()

    #                bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
    #                    threaded=False
    #                )
    #                return None



    if (n_times > 1) and (n_points < 2) and (n_levels <= 1):

        if type(vars) is str:
            vars = [vars]

        df = self.to_xarray()

        dim_dict = dict(df.dims)
        to_go = []
        for kk in dim_dict.keys():
            if dim_dict[kk] == 1:
                df = df.squeeze(kk)
                to_go.append(kk)

        df = df.to_dataframe()
        keep = self.variables
        df = df.reset_index()

        to_go = [x for x in df.columns if (x not in ["time"] and x not in keep)]

        df = df.drop(columns=to_go).drop_duplicates()

        if panel:
            intplot = (
                df.set_index("time")
                .loc[:, vars]
                .reset_index()
                .melt("time")
                .set_index("time")
                .hvplot(
                    by="variable",
                    logy=log,
                    subplots=True,
                    shared_axes=False,
                    responsive=(in_notebook() is False),
                )
            )
            if in_notebook():
                return intplot

            t = Thread(target=ctrc)
            t.start()

            bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
                threaded=False
            )
            return None

        else:
            intplot = (
                df.reset_index()
                .set_index("time")
                .loc[:, vars]
                .reset_index()
                .melt("time")
                .set_index("time")
                .hvplot(
                    groupby="variable",
                    logy=log,
                    dynamic=True,
                    responsive=(in_notebook() is False),
                )
            )
            if in_notebook():
                return intplot

            t = Thread(target=ctrc)
            t.start()

            bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
                threaded=False
            )
            return None


    if (n_points > 1) and (n_levels <= 1) and (type(vars) is list):
        out = subprocess.run(
            "cdo griddes " + self.current,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        lon_name = [
            x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x
        ][-1].split(" ")[-1]
        lat_name = [
            x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x
        ][-1].split(" ")[-1]

        if is_curvilinear(self.current):
            intplot = self.to_xarray().hvplot.quadmesh(
                lon_name,
                lat_name,
                vars,
                dynamic=True,
                cmap="viridis",
                logz=log,
                responsive=in_notebook() is False,
            )
        else:
            intplot = self.to_xarray().hvplot.image(
                lon_name,
                lat_name,
                vars,
                dynamic=True,
                cmap="viridis",
                logz=log,
                responsive=in_notebook() is False,
            )

        if in_notebook():
            return intplot

        t = Thread(target=ctrc)
        t.start()
        bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
            threaded=False
        )
        return None

    if (n_points > 1):

        if type(vars) is list:
            warnings.warn(message = "Warning: Only the first variable is mapped")
            vars = vars[0]

        out = subprocess.run(
            "cdo griddes " + self.current,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        lon_name = [
            x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x
        ][-1].split(" ")[-1]
        lat_name = [
            x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x
        ][-1].split(" ")[-1]

        self_max = self.to_xarray().rename({vars: "x"}).x.max()
        self_min = self.to_xarray().rename({vars: "x"}).x.min()
        v_max = max(self_max.values, -self_min.values)
        if (self_max.values > 0) and (self_min.values < 0):
            if is_curvilinear(self.current):
                intplot = (
                    self.to_xarray()
                    .hvplot.quadmesh(
                        lon_name,
                        lat_name,
                        vars,
                        dynamic=True,
                        logz=log,
                        responsive=(in_notebook() is False),
                    )
                    .redim.range(**{vars: (-v_max, v_max)})
                )
            else:
                intplot = (
                    self.to_xarray()
                    .hvplot.image(
                        lon_name,
                        lat_name,
                        vars,
                        dynamic=True,
                        logz=log,
                        responsive=(in_notebook() is False),
                    )
                    .redim.range(**{vars: (-v_max, v_max)})
                )
            if in_notebook():
                return intplot

            t = Thread(target=ctrc)
            t.start()
            bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
                threaded=False
            )
            return None

        else:
            if is_curvilinear(self.current):
                intplot = (
                    self.to_xarray()
                    .hvplot.quadmesh(
                        lon_name,
                        lat_name,
                        vars,
                        dynamic=True,
                        logz=log,
                        cmap="viridis",
                        responsive=(in_notebook() is False),
                    )
                    .redim.range(**{vars: (self_min.values, v_max)})
                )
            else:
                intplot = (
                    self.to_xarray()
                    .hvplot.image(
                        lon_name,
                        lat_name,
                        vars,
                        dynamic=True,
                        logz=log,
                        cmap="viridis",
                        responsive=(in_notebook() is False),
                    )
                    .redim.range(**{vars: (self_min.values, v_max)})
                )

            if in_notebook():
                return intplot

            t = Thread(target=ctrc)
            t.start()
            bokeh_server = pn.panel(intplot, sizing_mode="stretch_both").show(
                threaded=False
            )

            return None

    # Throw an error if case has not plotting method available yet
    # right now this only seems to be when you have lon/lat/time/levels and multiple variables
    # maybe needs an appropriate


    raise ValueError("Autoplotting method for this type of data is not yet available!")
