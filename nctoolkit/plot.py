
from ncplot import ncplot


def plot(self, vars=None, log=False, panel=False):

    """
    Autoplotting method.
    Automatically plot a dataset.

    Parameters
    -------------
    log: boolean
        Do you want a plotted data to be logged?
    vars: str or list
        A string or list of the variables to plot
    panel: boolean
        Do you want a panel plot, if avaiable?
    """

    if type(log) is not bool:
        raise TypeError("log is not boolean")

    if type(panel) is not bool:
        raise TypeError("panel is not boolean")

    self.run()

    if type(self.current) is list:
        raise TypeError("You cannot view multiple files!")

    return ncplot(self.current)

