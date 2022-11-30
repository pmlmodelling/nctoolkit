from nctoolkit.runthis import run_this

def align(self, align = "right"):
    """
    Method to align output time in temporal methods. 

    Parameters
    -------------
    align = str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    """
    
    if not isinstance(align, str):
        raise TypeError("Alignment must be str type")

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

    if align not in ["first","middle","last", "midhigh"]:
        raise ValueError(f"{align} is not a valid align argument")

    new_align = f"--timestat_date {align}"
    if len(self._align) > 0:
        if self._align != new_align:
            self.run()

    self._align = new_align 

def rollstat(self, window=None, stat="mean"):
    """Method to calculate the monthly statistic from a netCDF file"""

    # check alignment

    # check window supplied is valid

    if window is None:
        raise ValueError("No window was supplied")

    if not isinstance(window, int):
        raise TypeError("The window supplied is not numeric!")

    if window < 1:
        raise ValueError(f"{window} is not a valid window!")

    # create the cdo call and run it
    cdo_command = f"cdo -run{stat},{str(window)}"
    run_this(cdo_command, self, output="ensemble")


def rolling_mean(self, window=None, align = "right"):
    """
    Calculate a rolling mean based on a window

    Parameters
    -------------
    window: int
        The size of the window for the calculation of the rolling mean
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

         

    Examples
    ------------

    If you wanted to calculate a rolling mean with the mean calculated over every 10 time steps, do the following:

    >>> ds.rolling_mean(10)

    """
    self.align(align)
    rollstat(self, window=window, stat="mean")


def rolling_min(self, window=None, align = "right"):
    """
    Calculate a rolling minimum based on a window

    Parameters
    -------------
    window: int
        The size of the window for the calculation of the rolling minimum
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------

    If you wanted to calculate a rolling minimum with the minimum calculated over every 10 time steps, do the following:

    >>> ds.rolling_min(10)
    """
    self.align(align)
    rollstat(self, window=window, stat="min")


def rolling_max(self, window=None, align = "right"):
    """
    Calculate a rolling maximum based on a window

    Parameters
    -------------
    window: int
        The size of the window for the calculation of the rolling maximum
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"
    Examples
    ------------

    If you wanted to calculate a rolling maximum with the maximum calculated over every 10 time steps, do the following:

    >>> ds.rolling_max(10)
    """
    self.align(align)
    rollstat(self, window=window, stat="max")


def rolling_range(self, window=None, align = "right"):
    """
    Calculate a rolling range based on a window

    Parameters
    -------------
    window: int
        The size of the window for the calculation of the rolling range
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------

    If you wanted to calculate a rolling range with the range calculated over every 10 time steps, do the following:

    >>> ds.rolling_range(10)
    """
    self.align(align)
    rollstat(self, window=window, stat="range")


def rolling_sum(self, window=None, align = "right"):
    """
    Calculate a rolling sum based on a window

    Parameters
    -------------
    window: int
        The size of the window for the calculation of the rolling sum
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------

    If you wanted to calculate a rolling sum with the sum calculated over every 10 time steps, do the following:

    >>> ds.rolling_sum(10)
    """
    self.align(align)
    rollstat(self, window=window, stat="sum")

def rolling_var(self, window=None, align = "right"):
    """
    Calculate a rolling variance based on a window

    Parameters
    -------------
    window: int
        The size of the window for the calculation of the rolling sum
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------

    If you wanted to calculate a rolling variance with the variance calculated over every 10 time steps, do the following:

    >>> ds.rolling_sum(10)
    """
    self.align(align)
    rollstat(self, window=window, stat="var")

def rolling_stdev(self, window=None, align = "right"):
    """
    Calculate a rolling standard deviation based on a window

    Parameters
    -------------
    window: int
        The size of the window for the calculation of the rolling sum
    align: str
        This determines whether the output time is at the left, centre or right hand side of the time window.
        Options are "left", "centre" and "right"

    Examples
    ------------

    If you wanted to calculate a rolling standard deviation with the standard deviation calculated over every 10 time steps, do the following:

    >>> ds.rolling_sum(10)
    """
    self.align(align)
    rollstat(self, window=window, stat="std")
