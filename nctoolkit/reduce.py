from nctoolkit.runthis import run_this


def reduce_dims(self):
    """
    Reduce dimensions of data
    This will remove any dimensions with only one value. For example, if only selecting
    one vertical level, the vertical dimension will be removed.

    Examples
    ------------
    If you want to remove any dimensions that have only one value, do the following:

        >>> ds.reduce_dims("out.nc")

    Note that this will work lazily. This method is most useful when you want to simplify
    datasets before exporting them to something like a pandas dataframe.


    """

    if len(self.history) == len(self._hold_history):
        cdo_command = "cdo --reduce_dim copy"
    else:
        cdo_command = "cdo --reduce_dim"

    run_this(cdo_command, self, output="ensemble")
