import os
from ._runthis import run_this
from .flatten import str_flatten
from ._cleanup import cleanup

def time_interp(self, start_date = None, end_date = None, resolution = "monthly",  silent = True, cores = 1):

    """
    Temporally interpolate variables based on date range and time resolution 

    Parameters
    -------------
    start_data : str
        Start date for interpolation. Needs to be of the form YYYY/MM/DD or YYYY-MM-DD
    end_data : str
        End date for interpolation. Needs to be of the form YYYY/MM/DD or YYYY-MM-DD
    resolution : str
        Time steps used for intpoleration. Needs to be "daily", "weekly", "monthly" or "yearly"
    cores: int
        Number of cores to use if files are processed in parallel. Defaults to non-parallel operation 

    Returns
    -------------
    nchack.NCTracker
        Reduced tracker with the time interpolated data 
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
        if type(self.current) is list:
            ff = self.current[0]
            print("Warning: start date taken from first file in tracker!")
        else:
            ff = self.current
        cdo_command = "cdo showdate " + ff
        start_date = os.popen(cdo_command).read().strip().split(" ")[0]

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
