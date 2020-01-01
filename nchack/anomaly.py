
import copy
from .temp_file import temp_file
from .session import nc_safe
from .session import session_info
from .runthis import run_cdo
from .cleanup import cleanup


def annual_anomaly(self, baseline = None, metric = "absolute", window = 1):
    """
    Calculate annual anomalies based on a baseline period
    The anomaly is derived by first calculating the climatological mean for the given baseline period. Annual means are then calculated for each year and the anomaly is calculated compared with the baseline mean.

    Parameters
    -------------
    baseline: list
        Baseline years. This needs to be the first and last year of the climatological period. Example: a baseline of [1985,2005] will result in anomolies against  20 year climatology from 1986 to 2005.
    metric: str
        Set to "absolute" or "relative", depending on whether you want the absolute or relative anomaly to be calcualted.
    window: int
        A window for the anomaly. By default window = 1, i.e. the annual anomaly is calculated. If, for example, window = 20, the 20 year rolling means will be used to calculate the anomalies.
    """

    # This cannot possibly be threaded in cdo. Release it

    self.release()

    # throw an error if the dataset is an ensemble
    if type(self.current) is not str:
        raise TypeError("At present this only works for single files")

    # check baseline is a list, etc.
    if type(baseline) is not list:
        raise TypeError("baseline years supplied is not a list")
    if len(baseline) > 2:
        raise ValueError("More than 2 years in baseline. Please check.")
    if type(baseline[0]) is not int:
        raise TypeError("Provide a valid baseline")
    if type(baseline[1]) is not int:
        raise TypeError("Provide a vaid baseline")
    if len([yy for yy in baseline if yy not in self.years()]) > 0:
        raise ValueError("Check that the years in baseline are in the dataset!")
    if baseline[1] < baseline[0]:
        raise ValueError("Second baseline year is before the first!")

    # create the target file
    target = temp_file("nc")

    # check metric type
    if metric not in ["absolute", "relative"]:
        raise ValueError(metric + " is not a valid ype")

    # generate the cdo command
    if metric == "absolute":
        cdo_command = "cdo -L sub -runmean," + str(window) + " -yearmean " + self.current + " -timmean -selyear," + str(baseline[0]) + "/" + str(baseline[1]) + " " + self.current  + " " + target
    else:
        cdo_command = "cdo -L div -runmean," + str(window) + " -yearmean " + self.current + " -timmean -selyear," + str(baseline[0]) + "/" + str(baseline[1]) + " " + self.current  + " " + target

    # modify the cdo command if threadsafe
    if session_info["thread_safe"]:
        cdo_command = cdo_command.replace("-L "," ")

    # run the command and save the temp file
    target = run_cdo(cdo_command, target)

    # update the history
    self.history.append(cdo_command)
    self._hold_history = copy.deepcopy(self.history)

    # update the safe lists and current file
    if self.current in nc_safe:
        nc_safe.remove(self.current)

    self.current = target
    nc_safe.append(target)


    cleanup()






def monthly_anomaly(self, baseline = None):
    """
    Calculate monthly anomalies based on a baseline period
    The anomaly is derived by first calculating the climatological monthly mean for the given baseline period. Monthly means are then calculated for each year and the anomaly is calculated compared with the baseline mean.

    Parameters
    -------------
    baseline: list
        Baseline years. This needs to be the first and last year of the climatological period. Example: a baseline of [1985,2005] will result in anomolies against  20 year climatology from 1986 to 2005.
    """

    # release if set to lazy

    self.release()

    # throw an error if the dataset is an ensemble
    if type(self.current) is not str:
        raise TypeError("At present this only works for single files")

    # check baseline is a list, etc.
    if type(baseline) is not list:
        raise TypeError("baseline years supplied is not a list")
    if len(baseline) > 2:
        raise ValueError("More than 2 years in baseline. Please check.")
    if type(baseline[0]) is not int:
        raise TypeError("Provide a valid baseline")
    if type(baseline[1]) is not int:
        raise TypeError("Provide a vaid baseline")

    if len([yy for yy in baseline if yy not in self.years()]) > 0:
        raise ValueError("Check that the years in baseline are in the dataset!")
    if baseline[1] < baseline[0]:
        raise ValueError("Second baseline year is before the first!")

    # create the target file
    target = temp_file("nc")


    cdo_command = "cdo -L -ymonsub -monmean " + self.current +  " -ymonmean  -selyear," + str(baseline[0]) + "/" + str(baseline[1]) + " " + self.current + " " + target

    # run the command and save the temp file
    target = run_cdo(cdo_command, target)

    # update the history
    self.history.append(cdo_command)
    self._hold_history = copy.deepcopy(self.history)

    # updat the safe lists and current file
    if self.current in nc_safe:
        nc_safe.remove(self.current)

    self.current = target
    nc_safe.append(target)



    cleanup()





