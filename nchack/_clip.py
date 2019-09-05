
import tempfile

from ._runthis import run_this
from .flatten import str_flatten
from ._filetracker import nc_created
from ._cleanup import cleanup

def clip(self, lon = [-180, 180], lat = [-90, 90], silent = True, cores = 1):
    """ Function to clip netcdf files, spatially"""
    if (type(lon) is not list) or (type(lat) is not list):
        raise ValueError("Check that lon/lat ranges are tuples")
    
    if(type(lon[0]) is float ) or ( type(lon[0]) is int) == False:
        raise ValueError("Check lon")
    
    if( type(lon[1]) is float ) or ( type(lon[1]) is int) == False:
        raise ValueError("Check lon")

    if( type(lat[0]) is float ) or ( type(lat[0]) is int) == False:
        raise ValueError("Check lat")
    
    if( type(lat[1]) is float ) or ( type(lat[1]) is int) == False:
        raise ValueError("Check lat")

    # now, clip to the lonlat box we need

    if lon[0] > -180 or lon[1] > 180 or lat[0] > -90 or lat[1] < 90:

        lat_box = str_flatten(lon + lat)
        cdo_command = ("cdo sellonlatbox," + lat_box)
        run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)

    return(self)
    
