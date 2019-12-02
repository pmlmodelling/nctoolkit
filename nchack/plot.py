from .runthis import run_this
from .flatten import str_flatten

import pandas as pd, numpy as np
import hvplot.pandas
import hvplot.xarray
import subprocess
import xarray as xr



def autoplot(self, log = False, panel = False):
    """
    Autoplotting method

    Parameters
    -------------
    panel: boolean
        Do you want a panel plot, if avaiable?
    """

    self.release()

    if type(self.current) is list:
        raise TypeError("You cannot view multiple files!")

    cdo_result = subprocess.run("cdo ngrids " + self.current, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    n_grids = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    if n_grids > 1:
        raise ValueError("Autoplot cannot work with multiple grids")

    cdo_result = subprocess.run("cdo nlevel " + self.current, shell = True,stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    n_levels = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    cdo_result = subprocess.run("cdo ntime " + self.current, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    n_times = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    cdo_result = subprocess.run("cdo ngridpoints " + self.current, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    n_points = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    decode_time = False
    if n_times >= 1:
        try:
            x = xr.open_dataset(self.current)
            decode_times = True
        except:
            decode_times = False

    # Case when there is only a single map to show

    if n_times <= 1 and n_points > 1 and n_levels <= 1 and len(self.variables) == 1:
            data = self.to_xarray()
            data = data.rename({self.variables[0]: "x"})
            return data.x.plot()


    # Case when all you can plot is a time series, but more than one variable

    if n_times > 1 and n_points < 2 and n_levels <= 1 and len(self.variables) == 1:

        out = subprocess.run("cdo griddes " + self.current, shell = True, stdout=subprocess.PIPE, stderr =subprocess.PIPE)
        lon_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x][0].split(" ")[-1]
        lat_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x][0].split(" ")[-1]
        data = self.to_xarray(decode_times = decode_times)
        data = data.squeeze([lon_name, lat_name])
        data = data.rename({self.variables[0]: "x"})
        return data.x.hvplot()

    if n_times > 1 and n_points < 2 and n_levels <= 1 and len(self.variables) > 1:

        df = self.to_xarray(decode_times = decode_times)

        dim_dict = dict(df.dims)
        to_go = []
        for kk in dim_dict.keys():
            if dim_dict[kk] == 1:
                df = df.squeeze(kk)
                to_go.append(kk)

        df = df.to_dataframe()
        df = df.drop(columns = to_go)

        if panel:
            return df.reset_index().set_index("time").loc[:, self.variables].reset_index().melt("time").set_index("time").hvplot(by = "variable", logy = log, subplots = True, shared_axes = False)
        else:
            return df.reset_index().set_index("time").loc[:, self.variables].reset_index().melt("time").set_index("time").hvplot(groupby = "variable", logy = log, dynamic = True)

    if n_points > 1 and n_levels <= 1 and len(self.variables) == 1:
        out = subprocess.run("cdo griddes " + self.current, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
        lon_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x][0].split(" ")[-1]
        lat_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x][0].split(" ")[-1]

        variables = self.variables
        self_max = self.to_xarray(decode_times = decode_times).rename({self.variables[0]: "x"}).x.max()
        self_min = self.to_xarray(decode_times = decode_times).rename({self.variables[0]: "x"}).x.min()
        v_max = max(self_max.values, -self_min.values)
        if self_max.values > 0 and self_min.values < 0:
            return self.to_xarray(decode_times = decode_times).hvplot.image(lon_name, lat_name, self.variables[0], dynamic = True,  logz = log, cmap = "seismic").redim.range(**{self.variables[0]:(-v_max,v_max)})
        else:
            return self.to_xarray(decode_times = decode_times).hvplot.image(lon_name, lat_name, self.variables[0], dynamic = True,  logz = log, cmap = "viridis").redim.range(**{self.variables[0]:(-self_min.values, v_max)})

    if n_points > 1 and n_levels <= 1 and len(self.variables) > 1:
        out = subprocess.run("cdo griddes " + self.current, shell = True, stdout=subprocess.PIPE, stderr =subprocess.PIPE)
        lon_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x][0].split(" ")[-1]
        lat_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x][0].split(" ")[-1]

        variables = self.variables
        return self.to_xarray(decode_times = decode_times).hvplot.image(lon_name, lat_name, variables, dynamic = True, cmap = "viridis", logz = log)



    # Throw an error if case has not plotting method available yet

    raise ValueError("Autoplot method for this type of data is not yet available!")



