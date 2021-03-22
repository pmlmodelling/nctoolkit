def plot(self, vars=None):
    from ncplot import view

    """
    Autoplotting method.
    Automatically plot a dataset.

    Parameters
    -------------
    vars: str or list
        A string or list of the variables to plot

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

    return view(self[0], vars=vars)
