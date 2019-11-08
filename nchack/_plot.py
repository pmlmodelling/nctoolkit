from ._runthis import run_this
from .flatten import str_flatten

import pandas as pd, numpy as np
import hvplot.pandas
import hvplot.xarray
import subprocess



def autoplot(self, log = False, panel = False): 
    """
    Autoplotting method 

    Parameters
    -------------
    panel: boolean
        Do you want a panel plot, if avaiable? 
    """

    if type(self.current) is list:
        raise ValueError("You cannot view multiple files!")

    cdo_result = subprocess.run("cdo ngrids " + self.current, shell = True, capture_output = True)
    n_grids = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    if n_grids > 1:
        raise ValueError("Autoplot cannot work with multiple grids")

    cdo_result = subprocess.run("cdo nlevel " + self.current, shell = True, capture_output = True)
    n_levels = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    cdo_result = subprocess.run("cdo ntime " + self.current, shell = True, capture_output = True)
    n_times = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])

    cdo_result = subprocess.run("cdo ngridpoints " + self.current, shell = True, capture_output = True)
    n_points = int(str(cdo_result.stdout).replace("b'", "").split("\\n")[0])


    # Case when all you can plot is a time series

    if n_times > 1 and n_points < 2 and n_levels <= 1:

        df = self.to_xarray().to_dataframe()

        if panel:
            return df.reset_index().melt("time").set_index("time").hvplot(by = "variable", logy = log, subplots = True)
        else:
            return df.reset_index().melt("time").set_index("time").hvplot(groupby = "variable", logy = log, dynamic = True)


    if n_points > 1 and n_levels <= 1:
        out = subprocess.run("cdo griddes " + self.current, shell = True, capture_output = True)
        lon_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x][0].split(" ")[-1]
        lat_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x][0].split(" ")[-1]

        variables = self.variables
        return self.to_xarray().hvplot.image(lon_name, lat_name, variables, dynamic = False, cmap = "viridis", logz = log)



    # Throw an error if case has not plotting method available yet

    raise ValueError("Autoplot method for this type of data is not yet available!")

