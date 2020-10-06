
import copy
import subprocess

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this, run_nco, tidy_command
from nctoolkit.temp_file import temp_file
from nctoolkit.session import nc_safe
import warnings





def clip(self, lon=[-180, 180], lat=[-90, 90], nco=False):
    """
    Crop to a rectangular longitude and latitude box

    Parameters
    -------------
    lon: list
        The longitude range to select. This must be two variables,
        between -180 and 180 when nco = False.
    lat: list
        The latitude range to select. This must be two variables,
        between -90 and 90 when nco = False.
    nco: boolean
        Do you want this to use NCO for clipping? Defaults to False,
        and uses CDO. Set to True if you want to call NCO.
        NCO is typically better at handling very large horizontal grids.
    """

    # check validity of lon/lat supplied
    if (type(lon) is not list) or (type(lat) is not list):
        raise TypeError("Check that lon/lat ranges are tuples")

    if len(lon) != 2:
        raise ValueError("lon is a list of more than 2 variables")

    if len(lat) != 2:
        raise ValueError("lat is a list of more than 2 variables")

    for ll in lon:
        if (type(ll) is not int) and (type(ll) is not float):
            raise TypeError(f"{ll} from lon is not a float or int")

    for ll in lat:
        if (type(ll) is not int) and (type(ll) is not float):
            raise TypeError(f"{ll} from lat is not a float or int")

    # now, clip to the lonlat box we need

    if lat[1] < lat[0]:
        raise ValueError("Check lat order")
    if lon[1] < lon[0]:
        raise ValueError("Check lon order")

    if nco is False:
        if (lon[0] >= -180) and (lon[1] <= 180) and (lat[0] >= -90) and (lat[1] <= 90):
            lat_box = str_flatten(lon + lat)
            cdo_command = "cdo -sellonlatbox," + lat_box
            cdo_command = tidy_command(cdo_command)

            run_this(cdo_command, self, output="ensemble")
            return None
        else:
            raise ValueError("The lonlat box supplied is not valid!")

    self.run()

    new_files = []
    new_commands = []

    for ff in self:

        # find the names of lonlat

        out = subprocess.run(
            f"cdo griddes {ff}",
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
        target = temp_file("nc")

        nco_command = (
            "ncea -d "
            + lat_name
            + ","
            + str(float(lat[0]))
            + ","
            + str(float(lat[1]))
            + " -d "
            + lon_name
            + ","
            + str(float(lon[0]))
            + ","
            + str(float(lon[1]))
            + " "
            + ff
            + " "
            + target
        )
        if lon == [-180, 180]:
            nco_command = (
                "ncea -d "
                + lat_name
                + ","
                + str(float(lat[0]))
                + ","
                + str(float(lat[1]))
                + " "
                + ff
                + " "
                + target
            )

        if lat == [-90, 90]:
            nco_command = (
                "ncea  -d "
                + lon_name
                + ","
                + str(float(lon[0]))
                + ","
                + str(float(lon[1]))
                + " "
                + ff
                + " "
                + target
            )

        target = run_nco(nco_command, target)

        new_commands.append(nco_command)

        new_files.append(target)

    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    cleanup()
    self.disk_clean()


# deprecate this in December 2020

def release(self):
    """
    Run all stored commands in a dataset
    """
    warnings.warn(message="Warning: release is deprecated. Use run!")

    # the first step is to set the run status to true

    if (self._execute is False) and (len(self.history) > len(self._hold_history)):
        self._execute = True

        cdo_command = "cdo "

        output_method = "ensemble"

        if self._merged:
            output_method = "one"

        run_this(cdo_command, self, output=output_method)

        self._merged = False

        self._execute = False
        self._zip = False

        if len(self._safe) > 0:
            for ff in self._safe:
                if ff in nc_safe:
                    nc_safe.remove(ff)

        self._safe = []

        cleanup()

        self._thredds = False




# deprecate this in January 2021
def select_timestep(self, times=None):
    """
    Select timesteps from a dataset

    Parameters
    -------------
    times : list or int
        time step(s) to select. For example, if you wanted the first time step
        set times=0.
    """
    warnings.warn(message="select_timestep is deprecated. Use select_seasons")

    if times is None:
        raise ValueError("Please supply times")

    if type(times) is range:
        times = list(times)

    if type(times) is not list:
        times = [times]

    for tt in times:
        if type(tt) is not int:
            raise TypeError(f"{tt} is not an int")
        if tt < 0:
            raise ValueError(f"{tt} is not a valid timestep")

    # all of the variables in months need to be converted to ints,
    # just in case floats have been provided

    times = [int(x) + 1 for x in times]
    times = [str(x) for x in times]
    times = str_flatten(times)

    cdo_command = f"cdo -seltimestep,{times}"

    run_this(cdo_command, self, output="ensemble")

# deprecate this in January 2021

def select_season(self, season=None):
    """
    Select season from a dataset

    Parameters
    -------------
    season : str
        Season to select. One of "DJF", "MAM", "JJA", "SON".
    """

    warnings.warn(message="select_season is deprecated. Use select_seasons")

    if season is None:
        raise ValueError("No season supplied")

    if type(season) is not str:
        raise TypeError("Invalid season supplied")

    if season not in ["DJF", "MAM", "JJA", "SON"]:
        raise ValueError("Invalid season supplied")

    cdo_command = f"cdo -select,season={season}"
    run_this(cdo_command, self, output="ensemble")
