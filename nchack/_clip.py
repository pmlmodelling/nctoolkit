
import tempfile

from ._runthis import run_this
from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup

def clip(self, lon_range = [-180, 180], lat_range = [-90, 90], silent = True, cores = 1):
    """ Function to clip netcdf files, spatially"""
    if (type(lon_range) is not list) or (type(lat_range) is not list):
        raise ValueError("Check that lon/lat ranges are tuples")
    
    if(type(lon_range[0]) is float ) or ( type(lon_range[0]) is int) == False:
        raise ValueError("Check lon_range")
    
    if( type(lon_range[1]) is float ) or ( type(lon_range[1]) is int) == False:
        raise ValueError("Check lon_range")

    if( type(lat_range[0]) is float ) or ( type(lat_range[0]) is int) == False:
        raise ValueError("Check lat_range")
    
    if( type(lat_range[1]) is float ) or ( type(lat_range[1]) is int) == False:
        raise ValueError("Check lat_range")

    # now, clip to the lonlat box we need

    if lon_range[0] > -180 or lon_range[1] > 180 or lat_range[0] > -90 or lat_range[1] < 90:

        lat_box = str_flatten(lon_range + lat_range)
        cdo_command = ("cdo sellonlatbox," + lat_box)
        run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    
