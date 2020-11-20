
from ncplot import ncplot


def plot(self, vars=None):

    """
    Autoplotting method.
    Automatically plot a dataset.

    Parameters
    -------------
    vars: str or list
        A string or list of the variables to plot
    """

    self.run()

    if type(self.current) is list:
        raise TypeError("You cannot view multiple files!")

    return ncplot(self.current, vars = vars)

