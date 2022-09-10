import copy
import subprocess
import warnings
import os

from nctoolkit.api import open_data
from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this, run_cdo
from nctoolkit.temp_file import temp_file
from nctoolkit.session import append_safe
from nctoolkit.session import remove_safe

def to_zlevels(self, levels = None, thickness = None, depths = None):
    """
    Convert datasets with non z-level verticals to z-levels 
    Experimental method: Use at your own risk.


    Parameters
    -------------
    levels: list
        List of new z-levels. Must be positive and in metres.
    thickness: str or Dataset
        One of: a variable, in the dataset, which contains the variable thicknesses; a .nc file which contains
        the thicknesses; or a Dataset that contains the thicknesses. Note: the .nc file or Dataset must only contain
        one variable. Thickness should be in metres. Vertical interpolation will take the value from the mid-point of the level.
    depths: str or Dataset
        One of: a variable, in the dataset, which contains the depths of each cell; a .nc file which contains
        the depths; or a Dataset that contains the depths. Note: the .nc file or Dataset must only contain
        one variable.
    """
    self.run()

    if len(self) > 1:
        raise ValueError("This currently only works on single file datasets")

    if thickness is None and depths is None:
        if "e3t" in self.variables:
            thickness = "e3t"

    drop_this = None

    if depths is None:
        if "api.DataSet" not in str(type(thickness)):
            if thickness is None or type(thickness) is not str:
                raise ValueError("Please provide a valid thickness or depths variable")

    if thickness is None:
        if "api.DataSet" not in str(type(depths)):
            if depths is None or type(depths) is not str:
                raise ValueError("Please provide a valid thickness or depths variable")

    # Set up the thickness

    self1 = self.copy()
    ds = self.copy()

    ds.subset(variables=ds.contents.query("nlevels > 1").variable)
    ds.run()
    vars = ds.variables

    sorted = False

    if depths is None:

        if "api.DataSet" in str(type(thickness)):
            ds_depths = thickness.copy()
            ds_depths.run()
            if len(ds_depths.variables) != 1:
                raise ValueError("Please provide a thickness dataset with 1 variable!")
            sorted = True

        if sorted is False:
            if thickness in self.variables:
                ds_depths = open_data(self1[0])
                ds_depths.subset(variable=thickness)
                ds_depths.run()
                drop_this = thickness
            else:
                ds_depths = open_data(thickness)
                if len(ds_depths.variables) != 1:
                    raise ValueError("Please provide a thickness file with 1 variable!")

        thick_var = ds_depths.variables[0]

        ds_depths.rename({thick_var: "thickness"})
        ds_depths.run()
        ds_depths.vertical_cumsum()
        ds_depths.rename({"thickness": "depth"})
        ds_depths.subset(times = 0)
        ds_depths.cdo_command("setmisstoc,-9999999")
        ds_depths.run()

    if depths is not None:
        if "api.DataSet" in str(type(depths)):
            ds_depths = depths.copy()
            ds_depths.cdo_command("setmisstoc,-9999999")
            ds_depths.run()
            if len(ds_depths.variables) != 1:
                raise ValueError("Please provide a depths dataset with 1 variable!")
            sorted = True

        if sorted is False:
            if thickness in self.variables:
                ds_depths = open_data(self1[0])
                ds_depths.subset(variable=thickness)
                ds_depths.cdo_command("setmisstoc,-9999999")
                ds_depths.run()
                drop_this = thickness
            else:
                ds_depths = open_data(depths)
                ds_depths.cdo_command("setmisstoc,-9999999")
                ds_depths.run()
                if len(ds_depths.variables) != 1:
                    raise ValueError("Please provide a thickness file with 1 variable!")


    zaxis = temp_file().replace(".", "")
    append_safe(zaxis)


    line3 = "levels = " + " ".join([str(x) for x in levels]) + " \n"
    with open(zaxis, 'a') as the_file:
        x = the_file.write('zaxistype = depth_below_sea \n')
        x = the_file.write(f'size = {len(levels)} \n')
        x = the_file.write(line3)


    target = ds_depths.copy()
    target.assign(depth = lambda x: level(x.depth) + 0 * (x.depth == x.depth), drop = True)
    target.rename({"depth_2":"depth"})
    target.vertical_interp(levels = levels)
    target.run()

    out = temp_file(".nc")
    append_safe(out)

    command = f"cdo intlevel3d,{target[0]} {ds[0]}  {ds_depths[0]} {out}"

    run_cdo(command, target = out, precision = self._precision)

    test = open_data(out)
    test.cdo_command(f"setzaxis,{zaxis}")
    test.subset(variables = vars)
    test.run()
    self.current = test.current

    remove_safe(out)
    remove_safe(zaxis)

