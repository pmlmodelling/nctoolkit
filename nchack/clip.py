from .runthis import run_this
from .runthis import run_nco
from .temp_file import temp_file
from .flatten import str_flatten
from .session import nc_safe
import subprocess

def clip(self, lon = [-180, 180], lat = [-90, 90], cdo = True):
    """
    Clip to a rectangular longitude and latitude box

    Parameters
    -------------
    lon: list
        The longitude range to select. This must be two variables, between -180 and 180.
    lat: list
        The latitude range to select. This must be two variables, between -90 and 90.
    cdo: boolean
        Do you want this to use CDO or NCO for clipping? Defaults to True. Set to False if you want to call NCO. NCO is better at handling very large horizontal grids.
    """

    if  type(lon) is not list or type(lat) is not list:
        raise TypeError("Check that lon/lat ranges are tuples")

    if ( type(lon[0]) is float  or  type(lon[0]) is int ) == False:
        raise TypeError("Check lon")

    if ( type(lon[1]) is float  or  type(lon[1]) is int ) == False:
        raise TypeError("Check lon")

    if ( type(lat[0]) is float  or  type(lat[0]) is int ) == False:
        raise TypeError("Check lat")

    if ( type(lat[1]) is float  or  type(lat[1]) is int ) == False:
        raise TypeError("Check lat")

    # now, clip to the lonlat box we need

    if lon[0] >= -180 and lon[1] <= 180 and lat[0] >= -90 and lat[1] <= 90:

        if cdo:
            lat_box = str_flatten(lon + lat)
            cdo_command = ("cdo -sellonlatbox," + lat_box)
            run_this(cdo_command, self, output = "ensemble")
        else:
            if type(self.current) is list:
                raise TypeError("This method only works for single files at present")
            self.release()

            out = subprocess.run("cdo griddes " + self.current, shell = True, capture_output = True)
            lon_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "xname" in x][0].split(" ")[-1]
            lat_name = [x for x in str(out.stdout).replace("b'", "").split("\\n") if "yname" in x][0].split(" ")[-1]
            target = temp_file("nc")

            nco_command = "ncea -d " + lat_name + "," + str(float(lat[0])) + "," + str(float(lat[1])) + " -d " + lon_name + "," + str(float(lon[0])) + "," + str(float(lon[1]))  + " " + self.current + " " + target
            target = run_nco(nco_command, target)
            self.history.append(nco_command)
            self._hold_history = copy.deepcopy(self.history)
            if self.current in nc_safe:
                nc_safe.remove(self.current)
            self.current = target
            nc_safe.append(self.current)
            self.run = lazy_eval == False
    else:
        raise ValueError("The lonlat box supplied is not valid!")




