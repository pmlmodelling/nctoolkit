

import warnings
import copy
import os
import pandas as pd
import subprocess
from datetime import datetime

from .runthis import run_this


def merge(self, match = ["year", "month", "day"]):

    """
    Merge a multi-file ensemble into a single file. Merging will occur based on the time steps in the first file. This will only be effective if either you want to merge files with the same times or multi-time files with single time files.

    Parameters
    -------------
    match: a list stating what must match in the netcdf files. Defaults to year/month/day. This list must be some combination of year/month/day. An error will be thrown if the elements of time in match do not match across all netcdf files. The only exception is if there is a single date file in the ensemble.

    """

    # Force a release if needed
    self.release()

    if type(self.current) is not list:
        warnings.warn(message("There is only file in the dataset. No need to merge!"))
        return None

    if type(match) is list:
        match = [y.lower() for y in match]

    # Make sure the times in the files are compatiable, based on the match criteria

    all_times = []
    for ff in self.current:
        cdo_result = subprocess.run("cdo ntime " + ff, shell = True, capture_output = True)
        cdo_result = str(cdo_result.stdout)
        cdo_result = cdo_result.replace("b'", "").strip()
        ntime = int(cdo_result.split("\\")[0])
        all_times.append(ntime)
    if len(set(all_times)) > 1:
        warnings.warn(message = "The files to merge do not have the same number of time steps!")

    all_times = []
    for ff in self.current:
        cdo_result = subprocess.run("cdo showtimestamp " + ff, shell = True, capture_output = True)
        cdo_result = str(cdo_result.stdout)
        cdo_result = cdo_result.replace("b'", "").strip()
        cdo_result = cdo_result.split()
        cdo_result = pd.Series( (v for v in cdo_result) )
        all_times.append(cdo_result)

    for i in range(1, len(all_times)):
        if len(all_times[i]) != len(all_times[0]) and len(all_times[i]) > 1:
            raise ValueError("You are trying to merge data sets with an incompatible number of time steps")

    # remove files with more than one time step in it
    all_times = [x for x in all_times if len(x) > 1]

    all_df = []
    if len(all_times) > 1:
        for i in range(0, len(all_times)):
            month = [datetime.strptime(v[0:10], "%Y-%m-%d").month for v in all_times[i]]
            year = [datetime.strptime(v[0:10], "%Y-%m-%d").year for v in all_times[i]]
            day = [datetime.strptime(v[0:10], "%Y-%m-%d").day for v in all_times[i]]
            i_data = pd.DataFrame({"year":year, "month":month, "day":day})
            i_data = i_data.loc[:, match]
            all_df.append(i_data)

    for i in range(1, len(all_df)):
        if all_df[0].equals(all_df[i]) == False:
            raise ValueError("Dates of data sets do not satisfy matching criteria!")

    cdo_command = ("cdo -merge ")

    run_this(cdo_command, self, output = "one")

    self._merged = True



def merge_time(self):
    """
    Time-based merging of a multi-file ensemble into a single file
    This method is ideal if you have the same data split over multiple files covering different data sets.
    """

    self.release()

    if type(self.current) is not list:
        warnings.warn(message("There is only file in the dataset. No need to merge!"))
        return None

    if self._merged:
        raise ValueError("You cannot double chain merge methods!")

    cdo_command = "cdo --sortname -mergetime "

    run_this(cdo_command, self,  output = "one")

    self._merged = True

