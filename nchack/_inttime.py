from ._runthis import run_this
from .flatten import str_flatten
from ._cleanup import cleanup

def time_interp(self, start_date = None, end_date = None, resolution = "monthly",  silent = True, cores = 1):
    """Method to carry out time interplation
    Start and end dates must be of the format YYYY-MM-DD or YYYY/MM/DD
    """

    if resolution not in ["daily", "weekly", "monthly", "yearly"]:
        raise ValueError("Please supply a valid time resolution!")

    if resolution == "daily":
        resolution = "1day"

    if resolution == "weekly":
        resolution = "7day"

    if resolution == "monthly":
        resolution = "1month"

    if resolution == "yearly":
        resolution = "1year"
    
    if start_date is None:
        raise ValueError("No start date supplied")

    start_date = start_date.replace("/", "-")


    cdo_command = "-inttime,"+start_date +",12:00:00," + resolution

    if end_date is None:
        cdo_command = "cdo -L " + cdo_command
    else:
        end_date = end_date.replace("/", "-")
        cdo_command = "cdo -L " + "-seldate," + start_date + "," + end_date + " " + cdo_command

    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)

    # clean up the directory
    cleanup(keep = self.current)
