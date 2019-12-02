import subprocess
import warnings
def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

warnings.formatwarning = custom_formatwarning
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
        End date for interpolation. Needs to be of the form YYYY/MM/DD or YYYY-MM-DD
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
        if type(self.current) is list:
            ff = self.current[0]
            warnings.warn(message = "The start date taken from first file in data set!")
        else:
            ff = self.current
        cdo_command = "cdo showdate " + ff
        start =  subprocess.run(cdo_command, shell = True, stdout=subprocess.PIPE, stderr =subprocess.PIPE)
        start = str(start.stdout)
        start.replace("b'", "").strip().split(" ")[0]

    start = start.replace("/", "-")

    cdo_command = "-inttime,"+start +",12:00:00," + resolution

    if end is None:
        cdo_command = "cdo -L " + cdo_command
    else:
        end = end.replace("/", "-")
        cdo_command = "cdo -L " + "-seldate," + start + "," + end + " " + cdo_command

    run_this(cdo_command, self,  output = "ensemble")

