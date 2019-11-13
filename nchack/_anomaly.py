
import copy
from ._temp_file import temp_file
from ._session import nc_safe
from ._runthis import run_cdo

def annual_anomaly(self,  baseline = None, change = "absolute", window = 1):
    """

    Calculate annual anomalies based on a baseline period
    The anomoly is calculated by first calculating the climatological mean for the given baseline period. Annual means are then calculated for each year and the anomaly is calculated compared with the baseline mean.
    
    Parameters
    -------------
    baseline: list
        Baseline years. This needs to be the first and last year of the climatological period, Example [1985,2005] will give you a 20 year climatology from 1986 to 2005. 
    change: str
        Set to "absolute" or "relative", depending on whether you want the absolute or relative change to be calcualted.
    window: int
        A window for the anomaly. By default window = 1, i.e. the annual anomaly is calculated. If, for example, window = 20, the 20 year rolling means will be used to calculate the anomalies.

    """

    # release if set to lazy

    if self.run == False:
        lazy_eval = True
        self.release()
    else:
        lazy_eval = False

    if type(self.current) is not str:
        raise ValueError("Splitting the file by year did not work!")

    if type(baseline) is not list:
        raise ValueError("baseline years supplied is not a list")

    if len(baseline) > 2:
        raise ValueError("More than 2 years in baseline. Please check.")
    if type(baseline[0]) is not int:
        raise ValueError("Provide a valid baseline")
    if type(baseline[1]) is not int:
        raise ValueError("Provide a vaid baseline")

    target = temp_file("nc")

    if change == "absolute":
        cdo_command = "cdo -L sub -runmean," + str(window) + " -yearmean " + self.current + " -timmean -selyear," + str(baseline[0]) + "/" + str(baseline[1]) + " " + self.current  + " " + target
    else:
        cdo_command = "cdo -L div -runmean," + str(window) + " -yearmean " + self.current + " -timmean -selyear," + str(baseline[0]) + "/" + str(baseline[1]) + " " + self.current  + " " + target
        #cdo_command = "cdo -L div -yearmean " + self.current + " -timmean -selyear," + str(baseline[0]) + "/" + str(baseline[1]) + " " + self.current  + " " + target

    target = run_cdo(cdo_command, target)

    self.history.append(cdo_command)
    self.hold_history = copy.deepcopy(self.history)

    if self.current in nc_safe:
        nc_safe.remove(self.current)

    self.current = target
    nc_safe.append(target)


    if lazy_eval:
        self.run = False


