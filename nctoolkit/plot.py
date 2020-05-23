

from netCDF4 import Dataset

from threading import Thread


from nctoolkit.runthis import run_this
from nctoolkit.temp_file import temp_file
from nctoolkit.session import html_files

import time
import subprocess
import holoviews as hv
import panel as pn
import pandas as pd

hv.extension('bokeh')
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
    dataset = Dataset(ff)

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
    var_det = [
        ff.replace("Parameter name", "variable").split(" ") for ff in var_det
    ]
    sales = var_det[1:]
    labels = var_det[0]
    df = pd.DataFrame.from_records(sales, columns=labels)
    df = df.assign(Points = lambda x: x.Points.astype("int"))
    return df

def ctrc():
    time.sleep(1)
    print("Press Ctrl+C to stop plotting server")

# going to use show() to open plot in browser
import hvplot.pandas
import hvplot.xarray
from bokeh.plotting import show

import sys

def is_curvilinear(ff):
    """Function to work out if a file contains a curvilinear grid"""
    cdo_result = subprocess.run(
    f"cdo sinfo {ff}",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)

    return len([x for x in cdo_result.stdout.decode("utf-8").split("\n") if "curvilinear" in x]) > 0




def in_notebook():
    """
    Returns ``True`` if the module is running in IPython kernel,
    ``False`` if in IPython shell or other Python shell.
    """
    return 'ipykernel' in sys.modules



def plot(self, log=False, vars=None, panel=False):

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


    # Case when all you can plot is a time series, but more than one variable

    if (n_times > 1) and (n_points < 2) and (n_levels <= 1) and (type(vars) is str):

        out = subprocess.run(
            "cdo griddes " + self.current,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        lon_name = [
            x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x
        ][0].split(" ")[-1]
        lat_name = [
            x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x
        ][0].split(" ")[-1]
        data = self.to_xarray()
        data = data.squeeze([lon_name, lat_name])
        data = data.rename({vars: "x"})

        intplot =  data.x.hvplot(responsive = (in_notebook() == False))
        if in_notebook() == True:
            return intplot

        t = Thread(target = ctrc)
        t.start()

        bokeh_server = pn.panel(intplot, sizing_mode='stretch_both').show(threaded = False)

        return None

    if (n_times > 1) and (n_points < 2) and (n_levels <= 1) and (type(vars) is list):

        df = self.to_xarray()

        dim_dict = dict(df.dims)
        to_go = []
        for kk in dim_dict.keys():
            if dim_dict[kk] == 1:
                df = df.squeeze(kk)
                to_go.append(kk)

        df = df.to_dataframe()
        df = df.drop(columns=to_go)

        if panel:
            intplot =  (
                df.reset_index()
                .set_index("time")
                .loc[:, vars]
                .reset_index()
                .melt("time")
                .set_index("time")
                .hvplot(by="variable", logy=log, subplots=True, shared_axes=False, responsive = (in_notebook() == False))
            )
            if in_notebook():
                return intplot

            t = Thread(target = ctrc)
            t.start()

            bokeh_server = pn.panel(intplot, sizing_mode='stretch_both').show(threaded = False)
            return None

        else:
            intplot =  (
                df.reset_index()
                .set_index("time")
                .loc[:, vars]
                .reset_index()
                .melt("time")
                .set_index("time")
                .hvplot(groupby="variable", logy=log, dynamic=True, responsive = (in_notebook() == False))
            )
            if in_notebook():
                return intplot

            t = Thread(target = ctrc)
            t.start()

            bokeh_server = pn.panel(intplot, sizing_mode='stretch_both').show(threaded = False)
            return None

    if (n_points > 1) and (type(vars) is str):
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
                intplot =  self.to_xarray().hvplot.quadmesh(
                        lon_name, lat_name, vars, dynamic=True, logz=log,  responsive = (in_notebook() == False)).redim.range(**{vars: (-v_max, v_max)})
            else:
                intplot =  self.to_xarray().hvplot.image(
                        lon_name, lat_name, vars, dynamic=True, logz=log,  responsive = (in_notebook() == False)).redim.range(**{vars: (-v_max, v_max)})
            if in_notebook():
                return intplot

            t = Thread(target = ctrc)
            t.start()
            bokeh_server = pn.panel(intplot, sizing_mode='stretch_both').show(threaded = False)
            return None

        else:
            if is_curvilinear(self.current):
                intplot =  (
                    self.to_xarray()
                    .hvplot.quadmesh(
                        lon_name, lat_name, vars, dynamic=True, logz=log, cmap="viridis", responsive = (in_notebook() == False)
                    )
                    .redim.range(**{vars: (self_min.values, v_max)})
                )
            else:
                intplot =  (
                    self.to_xarray()
                    .hvplot.image(
                        lon_name, lat_name, vars, dynamic=True, logz=log, cmap="viridis", responsive = (in_notebook() == False)
                    )
                    .redim.range(**{vars: (self_min.values, v_max)})
                )

            if in_notebook():
                return intplot

            t = Thread(target = ctrc)
            t.start()
            bokeh_server = pn.panel(intplot, sizing_mode='stretch_both').show(threaded = False)


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
            intplot = ( self.to_xarray().hvplot.quadmesh(
                lon_name, lat_name, vars, dynamic=True, cmap="viridis", logz=log, responsive = in_notebook() == False
            ))
        else:
            intplot = ( self.to_xarray().hvplot.image(
                lon_name, lat_name, vars, dynamic=True, cmap="viridis", logz=log, responsive = in_notebook() == False
            ))

        if in_notebook():
            return intplot

        t = Thread(target = ctrc)
        t.start()
        bokeh_server = pn.panel(intplot, sizing_mode='stretch_both').show(threaded = False)
        return None


    # Throw an error if case has not plotting method available yet

    raise ValueError("Autoplotting method for this type of data is not yet available!")
