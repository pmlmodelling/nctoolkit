import copy
import warnings

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_nco
from nctoolkit.temp_file import temp_file
from nctoolkit.session import get_safe, remove_safe


def ensemble_percentile(self, p=None):
    """
    ensemble_percentile: Calculate an ensemble percentile.

    This will calculate the percentiles for each time step in the files.
    For example, if you had an ensemble of files where each file included
    12 months of data, it would calculate the percentile for each month.
    This operates on a grid cell by grid cell basis.

    Parameters
    -------------
    p : float or int
        percentile to calculate. 0<=p<=100.

    Examples
    -------------
    If you had an ensemble of climate models with data covering the same time steps, you would calculate the ensemble 90th percentile as follows:

    >>> ds.ensemble_percentile(p=90)

    """

    # make sure p is a number

    if p is None:
        raise ValueError("p was not supplied")

    if not isinstance(p, (int, float)):
        raise TypeError(f"p is a {type(p)}, not an int or float")

    # check p is between 0 and 100
    if (p < 0) or (p > 100):
        raise ValueError("p is not between 0 and 100!")

    # This method cannot possibly be chained. Release it
    self.run()

    # Throw an error if there is only a single file in the tracker
    if len(self) == 1:
        warnings.warn(message="There is only one file in the dataset")

    # create the cdo command and run it
    cdo_command = f"--sortname -enspctl,{p}"
    self.cdo_command(cdo_command, ensemble=True)

    # set the _merged attribute to True
    self._merged = True


def ensemble_nco(self, method, ignore_time=False):
    """
    NCO Method to calculate an ensemble stat from a list of files
    """
    self.run()

    ff_ensemble = copy.deepcopy(self.current)

    # generate a temp files
    target = temp_file("nc")

    # generate the nco call
    if ignore_time is False:
        nco_command = f'ncea -y {method} {str_flatten(ff_ensemble, " ")} {target}'
    else:
        nco_command = f'ncra -y {method} {str_flatten(ff_ensemble, " ")} {target}'

    # run the call
    target = run_nco(nco_command, target)

    remove_target = False
    if target in get_safe():
        remove_target = True

    # add the call to the history and tempfile to nc_safe
    self.history.append(nco_command)
    self._hold_history = copy.deepcopy(self.history)

    self.current = target

    if remove_target:
        remove_safe(target)

    self._merged = True

    cleanup()
    self.disk_clean()


def ensemble_stdev(self):
    """
    ensemble_stdev: Calculate an ensemble standard deviation

    The ensemble standard deviation is calculated for each time steps; for example, if the ensemble is made up of
    monthly files the standard deviation for each month will be calculated.
    This operates on a grid cell by grid cell basis.

    Examples
    -------------
    If you had an ensemble of climate models with data covering the same time steps, you would calculate the ensemble standard deviation as follows:

    >>> ds.ensemble_stdev()


    """

    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only one file in the dataset")

    cdo_command = "--sortname -ensstd"

    self.cdo_command(cdo_command, ensemble=True)


def ensemble_var(self):
    """
    ensemble_var: Calculate an ensemble variance

    The ensemble variance is calculated for each time steps; for example, if the ensemble is made up of
    monthly files the standard deviation for each month will be calculated.
    This operates on a grid cell by grid cell basis.

    Examples
    -------------
    If you had an ensemble of climate models with data covering the same time steps, you would calculate the ensemble variance as follows:

    >>> ds.ensemble_var()

    """

    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only one file in the dataset")

    cdo_command = "--sortname -ensvar"

    self.cdo_command(cdo_command, ensemble=True)

def ensemble_median(self):
    """
    ensemble_median: Calculate an ensemble median

    The ensemble median is calculated for each time steps; for example, if the ensemble is made up of
    monthly files the median for each month will be calculated.
    This operates on a grid cell by grid cell basis.

    Examples
    -------------
    If you had an ensemble of climate models with data covering the same time steps, you would calculate the ensemble median as follows:

    >>> ds.ensemble_median()

    """

    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only one file in the dataset")

    cdo_command = "--sortname -enspctl,50"

    self.cdo_command(cdo_command, ensemble=True)


def ensemble_max(self, nco=False, ignore_time=False):
    """
    ensemble_max: Calculate an ensemble maximum

    This operates on a grid cell by grid cell basis.

    Parameters
    -------------
    nco : boolean
        Do you want to use NCO for the calculation? Default is False, i.e. CDO is used.
        Modify default if run time is an issue.
    ignore_time : boolean
        If True the max is calculated over all time steps. If False, the ensemble max
        is calculated for each time steps; for example, if the ensemble is made up of
        monthly files the max for each month will be calculated.

    Examples
    -------------
    If you had an ensemble of climate models with data covering the same time steps, you would calculate the ensemble max as follows:

    >>> ds.ensemble_max()


    """

    if nco is False:
        self.run()

        if len(self) == 1:
            warnings.warn(message="There is only one file in the dataset")

        if ignore_time is False:
            cdo_command = "--sortname -ensmax"
        else:
            cdo_command = "-timmax --sortname -ensmax"

        self.cdo_command(cdo_command, ensemble=True)

        return None

    ensemble_nco(self, "max", ignore_time=ignore_time)


def ensemble_min(self, nco=False, ignore_time=False):
    """
    ensemble_min: Calculate an ensemble minimum.

    This operates on a grid cell by grid cell basis.

    Parameters
    -------------
    nco : boolean
        Do you want to use NCO for the calculation? Default is False, i.e. CDO is used.
        Modify default if run time is an issue.
    ignore_time : boolean
        If True the min is calculated over all time steps. If False, the ensemble min is
        calculated for each time steps; for example, if the ensemble is made up of
        monthly files the min for each month will be calculated.

    Examples
    -------------
    If you had an ensemble of climate models with data covering the same time steps, you would calculate the ensemble min as follows:

    >>> ds.ensemble_min()






    """
    if len(self) == 1:
        warnings.warn(message="There is only one file in the dataset")

    if nco is False:
        self.run()

        if ignore_time is False:
            cdo_command = "--sortname -ensmin"
        else:
            cdo_command = "-timmin --sortname -ensmin"

        self.cdo_command(cdo_command, ensemble=True)

        return None

    ensemble_nco(self, "min", ignore_time=ignore_time)


def ensemble_mean(self, nco=False, ignore_time=False):
    """
    ensemble_mean: Calculate an ensemble mean

    This operates on a grid cell by grid cell basis.

    Parameters
    -------------
    nco : boolean
        Do you want to use NCO for the calculation? Default is False, i.e. CDO is used.
        Modify default if run time is an issue.
    ignore_time : boolean
        If True the mean is calculated over all time steps. If False, the ensemble mean
        is calculated for each time steps; for example, if the ensemble is made up of
        monthly files the mean for each month will be calculated.

    Examples
    -------------
    If you had an ensemble of climate models with data covering the same time steps, you would calculate the ensemble mean as follows:
    ds.ensemble_mean()

    If you had an ensemble of files that covered different time steps and want to calculate the mean over all time steps, you would do the following:

    ds.ensemble_mean(ignore_time=True)


    """

    if nco is False:
        self.run()

        if len(self) == 1:
            warnings.warn(message="There is only one file in the dataset")

        if ignore_time is False:
            cdo_command = "--sortname -ensmean"
        else:
            cdo_command = "-timmean --sortname -ensmean"

        self.cdo_command(cdo_command, ensemble=True)

        return None

    ensemble_nco(self, "mean", ignore_time=ignore_time)


def ensemble_range(self):
    """
    ensemble_range: Calculate an ensemble range

    The range is calculated for each time step; for example, if each file in the
    ensemble has 12 months of data the statistic will be calculated for each month.

    This operates on a grid cell by grid cell basis.

    Examples
    -------------
    If you had an ensemble of climate models with data covering the same time steps, you would calculate the ensemble range as follows:

    >>> ds.ensemble_range()
    """
    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only one file in the dataset")

    cdo_command = "--sortname -ensrange"

    self.cdo_command(cdo_command, ensemble=True)


def ensemble_sum(self):
    """
    ensemble_sum: Calculate an ensemble sum

    The sum is calculated for each time step; for example, if each file in the
    ensemble has 12 months of data the statistic will be calculated for each month.

    This operates on a grid cell by grid cell basis.

    Examples
    -------------
    If you had an ensemble of climate models with data covering the same time steps, you would calculate the ensemble sum as follows:

    >>> ds.ensemble_sum()

    """
    self.run()

    if len(self) == 1:
        warnings.warn(message="There is only one file in the dataset")

    cdo_command = "--sortname -enssum"

    self.cdo_command(cdo_command, ensemble=True)
