from nctoolkit.runthis import run_this


def shift_hours(self, shift=None):
    """
    Shift times in dataset by a number of hours

    Parameters
    -------------
    shift: int
        Number of hours, positive or negative, to shift the time by.
    """

    if shift is None:
        raise ValueError("Please supply a shift value")

    if isinstance(shift, float):
        shift = int(shift)

    if not isinstance(shift, int):
        raise TypeError("Please supply an int for shift")

    cdo_command = f"cdo -shifttime,{shift}hour"

    run_this(cdo_command, self, output="ensemble")


def shift_days(self, shift=None):
    """
    Shift times in dataset by a number of days

    Parameters
    -------------
    shift: int
        Number of days, positive or negative, to shift the time by.
    """

    if shift is None:
        raise ValueError("Please supply a shift value")

    if isinstance(shift, float):
        shift = int(shift)

    if not isinstance(shift, int):
        raise TypeError("Please supply an int for shift")

    cdo_command = f"cdo -shifttime,{shift}days"

    run_this(cdo_command, self, output="ensemble")


def shift_months(self, shift=None):
    """
    Shift times in dataset by a number of months

    Parameters
    -------------
    shift: int
        Number of days, positive or negative, to shift the time by.
    """

    if shift is None:
        raise ValueError("Please supply a shift value")

    if isinstance(shift, float):
        shift = int(shift)

    if not isinstance(shift, int):
        raise TypeError("Please supply an int for shift")

    cdo_command = f"cdo -shifttime,{shift}months"

    run_this(cdo_command, self, output="ensemble")


def shift_years(self, shift=None):
    """
    Shift times in dataset by a number of years

    Parameters
    -------------
    shift: int
        Number of days, positive or negative, to shift the time by.
    """

    if shift is None:
        raise ValueError("Please supply a shift value")

    if isinstance(shift, float):
        shift = int(shift)

    if not isinstance(shift, int):
        raise TypeError("Please supply an int for shift")

    cdo_command = f"cdo -shifttime,{shift}years"

    run_this(cdo_command, self, output="ensemble")


def shift(self, **kwargs):
    """
    Shift method. A wrapper for shift_days, shift_hours
    Operations are applied in the order supplied.

    Parameters
    -------------
    *kwargs
        hours maps to shift_hours
        days maps to shift_days
        months maps to shift_months
        years maps to shift_years

        Note: this uses partial matches. So hour, day, month, year will also work.

    Examples
    ------------
    If you wanted to shift all times back 1 hour, you would do the following:

    >>> ds.shift(hours = -1)

    If you wanted to shift all times forward 2 days, you would do the following:

    >>> ds.shift(days = 2)

    If you wanted to shift all times forward 6 months, you would do the following:

    >>> ds.shift(months = 6)

    If you wanted to shift all times forward 1 year, you would do the following:

    >>> ds.shift(years = 1)

    This method will allow partial matches in arguments. So the following will do the same
    thing:

    >>> ds.shift(year = 2)

    >>> ds.shift(years = 2)

    """

    for key in kwargs:
        # if key not in valid_keys:

        if "day" in key:
            shift_days(self, kwargs[key])
            return None

        if "hour" in key:
            shift_hours(self, kwargs[key])
            return None

        if "mon" in key:
            shift_months(self, kwargs[key])
            return None

        if "year" in key:
            shift_years(self, kwargs[key])
            return None

    raise AttributeError(f"{key} is not a valid shifting method")
