from ._runthis import run_this
from .flatten import str_flatten

def clip(self, lon = [-180, 180], lat = [-90, 90], cores = 1):
    """
    Clip to a rectangular longitude and latitude lat box 

    Parameters
    -------------
    lon: list
        The longitude range to select. This must be two variables, within -180 and 180.    
    lat: list
        The latitude range to select. This must be two variables, within -90 and 90.    
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 
    """

    if  type(lon) is not list or type(lat) is not list:
        raise ValueError("Check that lon/lat ranges are tuples")
    
    if ( type(lon[0]) is float  or  type(lon[0]) is int ) == False:
        raise ValueError("Check lon")
    
    if ( type(lon[1]) is float  or  type(lon[1]) is int ) == False:
        raise ValueError("Check lon")

    if ( type(lat[0]) is float  or  type(lat[0]) is int ) == False:
        raise ValueError("Check lat")
    
    if ( type(lat[1]) is float  or  type(lat[1]) is int ) == False:
        raise ValueError("Check lat")

    # now, clip to the lonlat box we need

    if lon[0] >= -180 and lon[1] <= 180 and lat[0] >= -90 and lat[1] <= 90:

        lat_box = str_flatten(lon + lat)
        cdo_command = ("cdo -sellonlatbox," + lat_box)
        run_this(cdo_command, self, output = "ensemble", cores = cores)
    else:
        raise ValueError("The lonlat box supplied is not valid!")
