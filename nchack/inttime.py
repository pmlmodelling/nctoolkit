import subprocess
from .runthis import run_this
from .flatten import str_flatten

def time_interp(self, start = None, end = None, resolution = "monthly"):
    """
    Temporally interpolate variables based on date range and time resolution

    Parameters
    -------------
    start : str
        Start date for interpolation. Needs to be of the form YYYY/MM/DD or YYYY-MM-DD
    end : str
        End date for interpolation. Needs to be of the form YYYY/MM/DD or YYYY-MM-DD. If end is not given interpolation will be to the final available time in the dataset
    resolution : str
        Time steps used for intpoleration. Needs to be "daily", "weekly", "monthly" or "yearly"
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

    if start is None:
        raise ValueError("No start data supplied")

    start = start.replace("/", "-")

    cdo_command = "-inttime,"+start +",12:00:00," + resolution

    if end is None:
        cdo_command = "cdo -L " + cdo_command
    else:
        end = end.replace("/", "-")
        cdo_command = "cdo -L " + "-seldate," + start + "," + end + " " + cdo_command

    run_this(cdo_command, self,  output = "ensemble")

