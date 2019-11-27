
import copy
from .temp_file import temp_file
from .session import nc_safe
from .runthis import run_cdo

def annual_anomaly(self,  baseline = None, type = "absolute", window = 1):
    """

    Calculate annual anomalies based on a baseline period
    The anomaly is derived by first calculating the climatological mean for the given baseline period. Annual means are then calculated for each year and the anomaly is calculated compared with the baseline mean.

    Parameters
    -------------
    baseline: list
        Baseline years. This needs to be the first and last year of the climatological period, Example [1985,2005] will give you a 20 year climatology from 1986 to 2005.
    type: str
        Set to "absolute" or "relative", depending on whether you want the absolute or relative type to be calcualted.
    window: int
        A window for the anomaly. By default window = 1, i.e. the annual anomaly is calculated. If, for example, window = 20, the 20 year rolling means will be used to calculate the anomalies.

    """

    # release if set to lazy

    if self.run == False:
        self.release()
        self.run = False

    # throw an error if the dataset is an ensemble
    if type(self.current) is not str:
        raise ValueError("At present this only works for single files")

    # check baseline is a list, etc.
    if type(baseline) is not list:
        raise ValueError("baseline years supplied is not a list")
    if len(baseline) > 2:
        raise ValueError("More than 2 years in baseline. Please check.")
    if type(baseline[0]) is not int:
        raise ValueError("Provide a valid baseline")
    if type(baseline[1]) is not int:
        raise ValueError("Provide a vaid baseline")

    # create the target file
    target = temp_file("nc")

    # generate the cdo command
    if type == "absolute":
        cdo_command = "cdo -L sub -runmean," + str(window) + " -yearmean " + self.current + " -timmean -selyear," + str(baseline[0]) + "/" + str(baseline[1]) + " " + self.current  + " " + target
    else:
        cdo_command = "cdo -L div -runmean," + str(window) + " -yearmean " + self.current + " -timmean -selyear," + str(baseline[0]) + "/" + str(baseline[1]) + " " + self.current  + " " + target

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




