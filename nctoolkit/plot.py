def plot(self, vars=None, autoscale=True):
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

    if vars is None:
        if len(set(self.contents.nlevels)) > 1:
            raise ValueError(
                "Unable to plot datasets where variables have differing levels"
            )

    if type(vars) is str:
        vars = [vars]

    if type(vars) is not list:
        raise ValueError("vars must be a list")

    if type(vars) is list:
        if len(set(self.contents.query("variable in @vars").nlevels)) > 1:
            raise ValueError(
                "Unable to plot datasets where variables have differing levels"
            )

    return view(self[0], vars=vars, autoscale=autoscale)
