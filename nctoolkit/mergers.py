import pandas as pd
import subprocess
import warnings

from datetime import datetime

from nctoolkit.runthis import run_this
from nctoolkit.session import session_info


def cdo_version():
    """Function to find cdo version"""
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


def merge(self, match=["year", "month", "day"]):
    """
    Merge a multi-file ensemble into a single file
    Merging will occur based on the time steps in the first file.
    This will only be effective if you want to merge files with the same times,
    but with different variables.

    Parameters
    -------------
    match: list, str
        a list or str stating what must match in the netCDF files.
        Defaults to year/month/day. This list must be some combination of
        year/month/day. An error will be thrown if the elements of time in match
        do not match across all netCDF files. The only exception is if there is a
        single date file in the ensemble.
    """

    # basic checks on match criteria
    if type(match) is str:
        match = [match]

    if type(match) is not list:
        raise TypeError("match supplied is not a list")

    for mm in match:
        if type(mm) is not str:
            raise TypeError(f"{mm} from match is not a list")

    if type(match) is list:
        match = [y.lower() for y in match]

    if len([x for x in match if x not in ["year", "month", "day"]]) > 0:
        raise ValueError("match supplied is not valid")

    # Force a release if needed
    self.run()

    # If there is only a single file in the dataset, then nothing needs to be done
    if len(self) == 1:
        warnings.warn(
            message="There is only one file in the dataset. No need to merge!"
        )
        return None

    # Make sure the times in the files are compatiable, based on the match criteria

    all_times = []
    for ff in self:
        cdo_result = subprocess.run(
            f"cdo ntime {ff}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
        cdo_result = str(cdo_result).replace("b'", "").strip()
        ntime = int(cdo_result.split("\\")[0])
        all_times.append(ntime)
    if len(set(all_times)) > 1:
        warnings.warn(
            message="The files to merge do not have the same number of time steps!"
        )

    # we need to check the grids are the same
    all_grids = []
    for ff in self:
        cdo_result = subprocess.run(
            f"cdo griddes {ff}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
        all_grids.append(cdo_result)

    if len(set(all_grids)) > 1:
        raise ValueError(
            "The files in the dataset do not have the same grid. "
            "Consider using regrid!"
        )

    # check the file times are compatible
    all_times = []
    for ff in self:
        cdo_result = subprocess.run(
            f"cdo showtimestamp {ff}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
        cdo_result = str(cdo_result).replace("b'", "").strip()
        cdo_result = cdo_result.split()
        cdo_result = pd.Series((v for v in cdo_result))
        all_times.append(cdo_result)

    for i in range(1, len(all_times)):
        if (len(all_times[i]) != len(all_times[0])) and (len(all_times[i]) > 1):
            raise ValueError(
                "You are trying to merge data sets with an incompatible number "
                "of time steps"
            )

    # remove files with more than one time step in it
    all_times = [x for x in all_times if len(x) > 1]

    all_df = []
    if len(all_times) > 1:
        for i in range(0, len(all_times)):
            month = [datetime.strptime(v[0:10], "%Y-%m-%d").month for v in all_times[i]]
            year = [datetime.strptime(v[0:10], "%Y-%m-%d").year for v in all_times[i]]
            day = [datetime.strptime(v[0:10], "%Y-%m-%d").day for v in all_times[i]]
            i_data = pd.DataFrame({"year": year, "month": month, "day": day})
            i_data = i_data.loc[:, match]
            all_df.append(i_data)

    for i in range(1, len(all_df)):
        if all_df[0].equals(all_df[i]) is False:
            raise ValueError("Dates of data sets do not satisfy matching criteria!")

    cdo_command = "cdo -merge"

    run_this(cdo_command, self, output="one")

    if session_info["lazy"]:
        self._merged = True


def merge_time(self):
    """
    Time-based merging of a multi-file ensemble into a single file
    This method is ideal if you have the same data split over multiple
    files covering different data sets.
    """

    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only file in the dataset. No need to merge!")
        return None

    cdo_command = "cdo --sortname -mergetime"

    run_this(cdo_command, self, output="one")

    if session_info["lazy"]:
        self._merged = True




def collect(self):
    """
    Collect a dataset that has been split using distribute
    """

    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only file in the dataset. No need to merge!")
        return None

    cdo_command = "cdo -collgrid"

    run_this(cdo_command, self, output="one")

    if session_info["lazy"]:
        self._merged = True

    self.run()

