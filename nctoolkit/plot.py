


def plot(self, vars=None):
    from ncplot import view

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

    return view(self.current, vars = vars)

