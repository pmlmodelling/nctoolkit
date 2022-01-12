import pandas as pd
import subprocess
import warnings

from datetime import datetime

from nctoolkit.runthis import run_this
from nctoolkit.session import session_info
from nctoolkit.show import nc_variables, nc_times
from nctoolkit.utils import cdo_version, version_below, version_above

def below(x,y):
    x = x.split(".")
    x = int(x[0])* 1000 +  int(x[1]) * 100+  int(x[2])

    y = y.split(".")
    y = int(y[0])* 1000 +  int(y[1]) * 100+  int(y[2])

    return x < y

def merge(self, join="variables", match=["year", "month", "day"]):
    """
    Merge a multi-file ensemble into a single file
    2 methods are available. 1) merging files with different variables, but the same time steps.
    2) merging files with the same variables, with different times.

    Parameters
    -------------
    join: str
        This defines the type of merging to carry out. "variables": this will merge by variable, so that an ensemble
        with different variables, but the same number of time steps is merged to a single file.
        "time": this will merge files with the same variables, but different times to a single file, into a single file
        with ordered times.  join defaults to "variables", and uses partial matches, so "var" will give variable based merging.

    match: list, str
        Optional argument when join = 'variables'. A list or str stating what must match in the netCDF files.
        Defaults to year/month/day. This list must be some combination of
        year/month/day. An error will be thrown if the elements of time in match
        do not match across all netCDF files. The only exception is if there is a
        single date file in the ensemble.
    """
    if type(join) is not str:
        raise TypeError("join supplied is not a str")

    join_valid = False

    if join.startswith("var"):
        join_valid = True

    if join.startswith("time"):
        self.run()
        if version_below(cdo_version(), "1.9.9"):
            var_list = []
            var_com = []

            for ff in self:
                var_list += nc_variables(ff)
                var_com.append(nc_variables(ff))
            new_list = []

            for var in set(var_list):
                if len(var_com) == len([x for x in var_com if var in x]):
                    new_list.append(var)

            self.select(variables=new_list)
            self.run()

            removed = ",".join([x for x in set(var_list) if x not in new_list])
            if len([x for x in set(var_list) if x not in new_list]) > 0:
                warnings.warn(
                    f"The following variables are not in all files, so were ignored when merging: {removed}"
                )
                self.select(variables=new_list)
                self.run()

        if len(self) == 1:
            warnings.warn(
                message="There is only file in the dataset. No need to merge!"
            )
            return None

        cdo_command = "cdo --sortname -mergetime"

        run_this(cdo_command, self, output="one")

        if session_info["lazy"]:
            self._merged = True
        return None

    if join_valid == False:
        raise ValueError("join supplied is not valid")

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
        )
        cdo_result =  cdo_result.stdout.decode("utf-8")
        #.stdout
        #''cdo_result = str(cdo_result).replace("b'", "").strip()
        cdo_result = str(cdo_result)
        ntime = int(cdo_result.split("\n")[0])
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
        cdo_result = nc_times(ff)
        #    f"cdo showtimestamp {ff}",
        #    shell=True,
        #    stdout=subprocess.PIPE,
        #    stderr=subprocess.PIPE,
        #).stdout
        #cdo_result = str(cdo_result).replace("b'", "").strip()
        #cdo_result = cdo_result.split()
        #cdo_result = pd.Series((v for v in cdo_result))
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
            month = [v.month for v in all_times[i]]
            year = [v.year for v in all_times[i]]
            day = [v.day for v in all_times[i]]
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
