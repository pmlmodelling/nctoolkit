def time_interp(self, start=None, end=None, resolution="monthly"):
    """
    time_interp: Temporally interpolate variables based on date range and time resolution

    Parameters
    -------------
    start : str
        Start date for interpolation. Needs to be of the form YYYY/MM/DD or YYYY-MM-DD.
    end : str
        End date for interpolation. Needs to be of the form YYYY/MM/DD or YYYY-MM-DD.
        If end is not given interpolation will be to the final available time in the
        dataset.
    resolution : str
        Time steps used for interpolation. Needs to be "daily", "weekly", "monthly"
        or "yearly". Defaults to monthly.

    Examples
    -------------
    Interpolate from 01/01/2000 to 01/01/2001 to monthly data:

    >>> ds.time_interp(start="2000/01/01", end="2001/01/01", resolution="monthly")

    Interpolate from 01/01/2000 to 01/01/2001 to daily data:

    >>> ds.time_interp(start="2000/01/01", end="2001/01/01", resolution="daily")

    Interpolate from 01/01/2000 to 01/01/2001 to weekly data:

    >>> ds.time_interp(start="2000/01/01", end="2001/01/01", resolution="weekly")

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

    cdo_command = f"-inttime,{start},12:00:00,{resolution}"

    if end is None:
        cdo_command = f"{cdo_command}"
    else:
        end = end.replace("/", "-")
        cdo_command = f"-seldate,{start},{end} {cdo_command}"

    self.cdo_command(cdo_command, ensemble=False)


def timestep_interp(self, steps=None):
    """
    timestep_interp: Temporally interpolate a dataset to given number of time steps
    between existing time steps

    Parameters
    -------------
    steps : int
        Number of time steps to interpolate between existing time steps. For example,
        if you wanted to go from daily to hourly data you would set steps=24.

    Examples
    -------------
    Interpolate from daily to hourly data:

    >>> ds.timestep_interp(steps=24)

    """

    if not isinstance(steps, int):
        raise TypeError(f"{steps} is not an int!")

    if steps < 2:
        raise ValueError(f"{steps} is not greater than 1")

    cdo_command = f"-intntime,{steps}"

    self.cdo_command(cdo_command, ensemble=False)
