
import copy

from nctoolkit.cleanup import cleanup, disk_clean
from nctoolkit.runthis import run_cdo, tidy_command
from nctoolkit.session import nc_safe, session_info
from nctoolkit.show import nc_years
from nctoolkit.temp_file import temp_file


def annual_anomaly(self, baseline=None, metric="absolute", window=1):
    """
    Calculate annual anomalies for each variable based on a baseline period
    The anomaly is derived by first calculating the climatological annual mean for the given baseline period. Annual means are then calculated for each year and the anomaly is calculated compared with the baseline mean. This will be calculated on a per-file basis in a multi-file dataset.

    Parameters
    -------------
    baseline: list
        Baseline years. This needs to be the first and last year of the climatological period. Example: a baseline of [1980,1999] will result in anomalies against the 20 year climatology from 1980 to 1999.
    metric: str
        Set to "absolute" or "relative", depending on whether you want the absolute or relative anomaly to be calculated.
    window: int
        A window for the anomaly. By default window = 1, i.e. the annual anomaly is calculated. If, for example, window = 20, the 20 year rolling means will be used to calculate the anomalies.
    """

    if type(window) is not int:
        raise TypeError("window is not an int")

    if window <= 0:
        raise TypeError("window is not valid")

    # check baseline is a list, etc.
    if type(baseline) is not list:
        raise TypeError("baseline years supplied is not a list")
    if len(baseline) != 2:
        raise ValueError("Supply a 2 year baseline")
    if type(baseline[0]) is not int:
        raise TypeError("Provide a valid baseline")
    if type(baseline[1]) is not int:
        raise TypeError("Provide a vaid baseline")
    if baseline[1] < baseline[0]:
        raise ValueError("Second baseline year is before the first!")

    # check metric type
    if metric not in ["absolute", "relative"]:
        raise ValueError(f"{metric} is not a valid metric")

    # This cannot possibly be threaded in cdo. Release it

    self.run()

    # calculate the anomalies for each file
    # this is not parallelized yet
    # list of new files created
    new_files = []
    # list of new commands
    new_commands = []

    for ff in self:
        # create the target file
        target = temp_file("nc")

        # throw error if baseline is not valid
        if len([yy for yy in baseline if yy not in nc_years(ff)]) > 0:
            raise ValueError("Check that the years in baseline are in the dataset!")
        # generate the cdo command
        if metric == "absolute":
            cdo_command = f"cdo -sub -runmean,{window} -yearmean {ff} -timmean -selyear,{baseline[0]}/{baseline[1]} {ff} {target}"
        else:
            cdo_command = f"cdo -div -runmean,{window} -yearmean {ff} -timmean -selyear,{baseline[0]}/{baseline[1]} {ff} {target}"

        # run the command and save the temp file

        cdo_command = tidy_command(cdo_command)
        target = run_cdo(cdo_command, target)

        # updae the new files and commands
        new_files.append(target)
        new_commands.append(cdo_command)

    # update the history
    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    cleanup()

    self.disk_clean()


def monthly_anomaly(self, baseline=None):
    """
    Calculate monthly anomalies based on a baseline period
    The anomaly is derived by first calculating the climatological monthly mean for the given baseline period. Monthly means are then calculated for each year and the anomaly is calculated compared with the baseline mean. This is calculated separately for each file in a multi-file dataset.

    Parameters
    -------------
    baseline: list
        Baseline years. This needs to be the first and last year of the climatological period. Example: a baseline of [1985,2005] will result in anomolies against 20 year climatology from 1986 to 2005.
    """

    # check baseline is a list, etc.
    if type(baseline) is not list:
        raise TypeError("baseline years supplied is not a list")
    if len(baseline) != 2:
        raise ValueError("More than 2 years in baseline. Please check.")
    if type(baseline[0]) is not int:
        raise TypeError("Provide a valid baseline")
    if type(baseline[1]) is not int:
        raise TypeError("Provide a vaid baseline")
    if baseline[1] < baseline[0]:
        raise ValueError("Second baseline year is before the first!")

    self.run()

    new_files = []
    new_commands = []

    for ff in self:

        if len([yy for yy in baseline if yy not in nc_years(ff)]) > 0:
            raise ValueError("Check that the years in baseline are in the dataset!")
        # create the target file
        target = temp_file("nc")
        # create system command
        cdo_command = f"cdo -ymonsub -monmean {ff} -ymonmean -selyear,{baseline[0]}/{baseline[1]} {ff} {target}"

        cdo_command = tidy_command(cdo_command)

        # run the command and save the temp file
        target = run_cdo(cdo_command, target)

        new_files.append(target)
        new_commands.append(cdo_command)

    # update the history
    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    cleanup()
    self.disk_clean()
