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
        raise TypeError("Please supply a shift value")

    if type(shift) is float:
        shift = int(shift)

    if type(shift) is not int:
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
        raise TypeError("Please supply a shift value")

    if type(shift) is float:
        shift = int(shift)

    if type(shift) is not int:
        raise TypeError("Please supply an int for shift")

    cdo_command = f"cdo -shifttime,{shift}days"

    run_this(cdo_command, self, output="ensemble")
