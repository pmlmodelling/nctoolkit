from nctoolkit.session import session_info


def zip(self):
    """
    Zip the dataset
    This will compress the files within the dataset. This works lazily.

    Examples
    ------------
    If you want to zip the files in a dataset, do the following:

        >>> ds.zip()

    This will occur lazily, so will only occur after everything has been evaluated.

    """
    self._zip = True
    if session_info["lazy"] is False:
        self._execute = False
        self.run()
