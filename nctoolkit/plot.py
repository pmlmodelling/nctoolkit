import signal
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out. Try plotting fewer variables!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def plot(self, vars=None, autoscale=True, out = None, **kwargs):
    from ncplot import view

    """
    Autoplotting method.
    Automatically plot a dataset.

    Parameters
    -------------
    vars: str or list
        A string or list of the variables to plot

    out: str
        Name of output file if you want to save as html. Defaults to None.

    **kwargs: Optional args to be sent to hvplot
         

    Examples
    ------------

    If you want to plot all data in a dataset, do the following:

    >>> ds.plot()

    If you only want to plot a single variable, do the following. Note, this is often faster if you
    have a large dataset.

    >>> ds.plot("var_of_choice")

    """

    # run any commands
    self.run()

    if len(self) > 1:
        raise TypeError("You cannot view multiple files!")

    if vars is None:
        if len(set(self.contents.nlevels)) > 1:
            raise ValueError(
                "Unable to plot datasets when variables have differing levels"
            )

    if type(vars) is str:
        vars = [vars]

    if type(vars) is not list and vars is not None:
        raise ValueError("vars must be a list")

    if type(vars) is list:
        if len(set(self.contents.query("variable in @vars").nlevels)) > 1:
            raise ValueError(
                "Unable to plot datasets when variables have differing levels"
            )
    if vars is None and len(self.variables) > 1:
        with time_limit(20):
            return view(self[0], autoscale=autoscale, **kwargs)

    if type(vars) is list and len(vars) > 1:
        with time_limit(20):
            return view(self[0], vars=vars, autoscale=autoscale, **kwargs)

    return view(self[0], vars=vars, autoscale=autoscale, out = out, **kwargs)
