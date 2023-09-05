import copy
import platform
import os

from nctoolkit.api import open_data
from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_cdo, tidy_command
from nctoolkit.show import nc_years
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe, session_info, nc_safe_par, nc_safe
from nctoolkit.api import update_options

if platform.system() == "Linux":
    import multiprocessing as mp
    from multiprocessing import Manager

    manager = Manager()
else:
    import multiprocess as mp
    from multiprocess import Manager

    manager = Manager()


def ann_anomaly(
    ff, baseline, metric, window, align, precision, new_files, new_commands, nc_safe
):
    """
    Function to calculate the anomaly for a single file
    """

    # throw error if baseline is not valid
    orig_safe = copy.deepcopy(nc_safe)
    target = temp_file("nc")
    nc_safe.append(target)
    try:
        if len([yy for yy in baseline if yy not in nc_years(ff)]) > 0:
            raise ValueError("Check that the years in baseline are in the dataset!")

        # create the target file
        # generate the cdo command
        if metric == "absolute":
            cdo_command = (
                f"cdo -sub -runmean,{window} -yearmean {ff} -timmean "
                f"-selyear,{baseline[0]}/{baseline[1]} {ff} {target}"
            )
        else:
            cdo_command = (
                f"cdo -div -runmean,{window} -yearmean {ff} -timmean "
                f"-selyear,{baseline[0]}/{baseline[1]} {ff} {target}"
            )

        # run the command and save the temp file

        cdo_command = tidy_command(cdo_command)
        cdo_command = cdo_command.replace(
            "cdo ", f"cdo --timestat_date {align} "
        ).replace("  ", " ")

        target = run_cdo(cdo_command, target, precision=precision)
        if target not in nc_safe:
            nc_safe.append(target)

        # update the new files and commands
        new_files.append(target)
        new_commands.append(cdo_command)
    except BaseException as e:
        try:
            nc_safe.remove(target)
        except:
            pass
        return e


def annual_anomaly(self, baseline=None, metric="absolute", window=1, align="right"):
    """
    annual_anomaly: Calculate annual anomalies for each variable based on a baseline period.

    The anomaly is derived by first calculating the climatological annual mean for the
    given baseline period. Annual means are then calculated for each year and the
    anomaly is calculated compared with the baseline mean. This will be calculated on a
    per-file basis in a multi-file dataset.

    Parameters
    -------------
    baseline: list
        Baseline years. This needs to be the first and last year of the climatological
        period. Example: a baseline of [1980,1999] will result in anomalies against the
        20 year climatology from 1980 to 1999.
    metric: str
        Set to "absolute" or "relative", depending on whether you want the absolute or
        relative anomaly to be calculated.
    window: int
        A window for the anomaly. By default window = 1, i.e. the annual anomaly is
        calculated. If, for example, window = 20, the 20 year rolling means will be
        used to calculate the anomalies.

    Examples
    ------------

    If you wanted to calculate an annual anomaly where values are compared with the mean for the years
    1950-1969, you would do this:

    >>> ds.annual_anomaly(baseline = [1950, 1969])

    By default, this results in the absolute difference to be used. If you wanted the anomaly to be calculated
    relative to the baseline mean, you would do this:

    >>> ds.annual_anomaly(baseline = [1950, 1969], metric = "relative")

    You might want to smooth out the anomalies, so that you are looking at rolling averages. In that case you can
    supply a windows. So if you wanted to calculate the anomaly using a rolling average with a 10 year window, you
    would do this:

    >>> ds.annual_anomaly(baseline = [1950, 1969], window = 10)


    """

    if "cen" in align:
        align = "middle"

    if "left" in align:
        align = "first"

    if "right" in align:
        align = "last"

    if "last" in align:
        align = "last"

    if "first" in align:
        align = "first"

    if "middle" in align:
        align = "midhigh"

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    if not isinstance(window, int):
        raise TypeError("window is not an int")

    if window <= 0:
        raise TypeError("window is not valid")

    # check baseline is a list, etc.
    if not isinstance(baseline, list):
        raise TypeError("baseline years supplied is not a list")
    if len(baseline) != 2:
        raise ValueError("Supply a 2 year baseline")
    if not isinstance(baseline[0], int):
        raise TypeError("Provide a valid baseline")
    if not isinstance(baseline[1], int):
        raise TypeError("Provide a valid baseline")
    if baseline[1] < baseline[0]:
        raise ValueError("Second baseline year is before the first!")

    # check metric type
    if metric not in ["absolute", "relative"]:
        raise ValueError(f"{metric} is not a valid metric")

    # This cannot possibly be threaded in cdo. Release it

    self.run()

    # calculate the anomalies for each file
    # this is not parallelized yet
    # list of new files created
    new_files = manager.list()
    # list of new commands
    new_commands = manager.list()

    # keep track of whether we started parallel, so it can be reset
    start_parallel = session_info["parallel"]

    if start_parallel is False:
        update_options({"parallel": True})

    nc_safe_par_start = copy.deepcopy(nc_safe_par)
    try:
        # loop over the files and calculate the anomaly in parallel
        cores = session_info["cores"]

        target_list = []
        results = dict()

        pool = mp.pool.Pool(cores)
        precision = copy.deepcopy(self._precision)
        for ff in self:
            results[ff] = pool.apply_async(
                ann_anomaly,
                [
                    ff,
                    baseline,
                    metric,
                    window,
                    align,
                    precision,
                    new_files,
                    new_commands,
                    nc_safe_par,
                ],
            )
        for k, v in results.items():
            out = v.get()
            if "Check that the years in baseline are in the dataset!" in str(out):
                raise ValueError("Check that the years in baseline are in the dataset!")

        pool.close()
        pool.join()

        self.history += list(new_commands)
        self._hold_history = copy.deepcopy(self.history)

        if start_parallel is False:
            update_options({"parallel": False})
            while True:
                for ff in nc_safe_par:
                    if ff not in nc_safe:
                        nc_safe.append(ff)
                    nc_safe_par.remove(ff)
                if len(nc_safe_par) == 0:
                    break

        self.current = list(new_files)

        for ff in new_files:
            remove_safe(ff)

        if start_parallel is False:
            for ff in list(set(new_files)):
                while True:
                    if ff in nc_safe:
                        nc_safe.remove(ff)
                    else:
                        break
                nc_safe.append(ff)

        if start_parallel:
            for ff in list(set(new_files)):
                while True:
                    if ff in nc_safe_par:
                        nc_safe_par.remove(ff)
                    else:
                        break
                nc_safe_par.append(ff)

        cleanup()

        self.disk_clean()
    except BaseException as e:
        if start_parallel is False:
            update_options({"parallel": False})
        if start_parallel:
            for ff in nc_safe_par:
                if ff not in nc_safe_par_start:
                    nc_safe_par.remove(ff)
        else:
            for ff in nc_safe:
                if ff not in nc_safe_par_start:
                    nc_safe.remove(ff)
            for ff in nc_safe_par:
                nc_safe_par.remove(ff)

        raise e


def monthly_anomaly(self, baseline=None):
    """
    monthly:anomaly: Calculate monthly anomalies based on a baseline period.

    The anomaly is derived by first calculating the climatological monthly mean for the
    given baseline period. Monthly means are then calculated for each year and the
    anomaly is calculated compared with the baseline mean. This is calculated separately
    for each file in a multi-file dataset.

    Parameters
    -------------
    baseline: list
        Baseline years. This needs to be the first and last year of the climatological
        period. Example: a baseline of [1985,2005] will result in anomolies against 20
        year climatology from 1986 to 2005.

    Examples
    ------------

    If you wanted to calculate a monthly anomaly where values are compared with the climatological monthly mean
    for the years 1950-1969, you would do this:

    >>> ds.monthly_anomaly(baseline = [1950, 1969])

    """

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    # check baseline is a list, etc.
    if not isinstance(baseline, list):
        raise TypeError("baseline years supplied is not a list")
    if len(baseline) != 2:
        raise ValueError("More than 2 years in baseline. Please check.")
    if not isinstance(baseline[0], int):
        raise TypeError("Provide a valid baseline")
    if not isinstance(baseline[1], int):
        raise TypeError("Provide a vaid baseline")
    if baseline[1] < baseline[0]:
        raise ValueError("Second baseline year is before the first!")

    self.run()

    new_files = []
    new_commands = []

    for ff in self:
        if len([yy for yy in baseline if yy not in nc_years(ff)]) > 0:
            raise ValueError("Check that the years in baseline are in the dataset!")
        # create the target file
        target = temp_file("nc")
        # create system command
        cdo_command = (
            f"cdo -ymonsub -monmean {ff} -ymonmean -selyear,"
            f"{baseline[0]}/{baseline[1]} {ff} {target}"
        )

        cdo_command = tidy_command(cdo_command)

        # run the command and save the temp file
        target = run_cdo(cdo_command, target, precision=self._precision)

        new_files.append(target)
        new_commands.append(cdo_command)

    # update the history
    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    for ff in new_files:
        remove_safe(ff)

    cleanup()
    self.disk_clean()
