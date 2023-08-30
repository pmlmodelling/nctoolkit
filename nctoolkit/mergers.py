import pandas as pd
import subprocess
import warnings

from nctoolkit.session import session_info
from nctoolkit.show import nc_variables, nc_times
from nctoolkit.api import open_data


def chunks(l, n):
    n = max(1, n)
    return (l[i : i + n] for i in range(0, len(l), n))


import inspect
from functools import wraps


def check_checker(f):
    varnames = inspect.getfullargspec(f)[0]

    @wraps(f)
    def wrapper(*a, **kw):
        explicit_params = set(list(varnames[: len(a)]) + list(kw.keys()))
        if "check" not in explicit_params:
            kw["check"] = "default"
        return f(*a, **kw)

    return wrapper


@check_checker
def merge(self, join="variables", match=["year", "month", "day"], check=True):
    """
    merge: Merge a multi-file ensemble into a single file

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
    check: bool
        By default nctoolkit out checks in case files do not have the same variables etc. Set check to False if you are confident merging will be problem free.
        If you are unsure if files have the same variables, set check to True to find out. Note: if you do not explicitly provide check and there are more than 30
        files in a dataset, checks will be turned off.

    Examples
    -------------
    If you wanted to merge files with the same variables, but different time steps, you would do:
    >>> ds.merge(join='time')
    If you wanted to merge files with different variables, but the same time steps, you would do:
    >>> ds.merge(join='variables')

    If you wanted to merge files with different variables, but the same time steps, but only needed to ensure that the month in each time step matched, you would do:

    >>> ds.merge(join='variables', match='month')

    The above may be useful if you have a dataset with monthly data, but some files have the first of the month, and some have the 15th of the month.

    """

    if check == "default":
        if len(self) > 30:
            check = False
            warnings.warn(
                message="Large ensemble, so no checks are being carried out prior to merging. Set check=True if you require files to be checked for variable compatability!"
            )
        else:
            check = True

    if not isinstance(join, str):
        raise TypeError("join supplied is not a str")

    join_valid = False

    if join.startswith("var"):
        join_valid = True

    if join.startswith("time"):
        self.run()

        if len(self) == 1:
            warnings.warn(
                message="There is only file in the dataset. No need to merge!"
            )
            return None

        # check variable names are consistent

        if check:
            var_list = set()
            for ff in self:
                var_list.add(",".join(nc_variables(ff)))
            if len(var_list) > 1:
                raise ValueError(
                    "You are trying to merge files with different variables!"
                )

        cdo_command = "--sortname -mergetime"

        if len(self) < 400:
            self.cdo_command(cdo_command, ensemble=True)
        else:
            new_ds = open_data()
            files = chunks(self, 365)
            ii = 0
            for ff in files:
                ii += 1
                ds = open_data(ff, checks=False)
                ds.merge("time", check=check)
                ds.run()
                new_ds.append(ds)

            new_ds.merge("time", check=check)
            new_ds.run()
            self.current = new_ds.current

        if session_info["lazy"]:
            self._merged = True
        return None

    if join_valid is False:
        raise ValueError("join supplied is not valid")

    # basic checks on match criteria
    if isinstance(match, str):
        match = [match]

    if not isinstance(match, list):
        raise TypeError("match supplied is not a list")

    for mm in match:
        if not isinstance(mm, str):
            raise TypeError(f"{mm} from match is not a list")

    if isinstance(match, list):
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
        cdo_result = cdo_result.stdout.decode("utf-8")
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

    cdo_command = "-merge"
    self.cdo_command(cdo_command, ensemble=False)

    if session_info["lazy"]:
        self._merged = True


def collect(self):
    """
    Collect a dataset that has been split using distribute

    Examples
    --------
    >>> ds.distribute(4,4)
    >>> #... Carry out some operations
    >>> ds.collect()

    """

    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only file in the dataset. No need to merge!")
        return None

    cdo_command = "-collgrid"

    self.cdo_command(cdo_command, ensemble=True)

    if session_info["lazy"]:
        self._merged = True

    self.run()
