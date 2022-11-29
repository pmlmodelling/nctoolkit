import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_cdo, tidy_command
from nctoolkit.show import nc_variables
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe, get_safe
from nctoolkit.api import from_xarray


def open_shape(ff = None, res = None):
    """
    Calculate the correlation correct in time between two variables
    The correlation is calculated for each grid cell, ignoring missing values.

    Parameters
    -------------
    ff: str
        File path to shape file
    res: list
        x and y horizontal resolution 

    """
    if not isinstance(ff, str):
        raise ValueError("Please provide a file path")

    if not isinstance(res, list):
        raise ValueError("Please provide a list as resolution")
    if len(res) != 2:
        raise ValueError("Please provide a 2 variable list as res")

    from geocube.api.core import make_geocube
    import geopandas
    print("Attempting to convert shape file to netCDF using geocube!")
    shp = geopandas.read_file(ff)
    cube = make_geocube(
        shp,
        resolution=(res[0], res[1]),
    )
    ds = from_xarray(cube)
    return ds
