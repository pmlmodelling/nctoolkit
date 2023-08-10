from nctoolkit.session import session_info


def zip(self):
    """
    zip: Zip the dataset

    This will compress the files within the dataset.

    This will occur lazily, so will only occur after everything has been evaluated.

    Examples
    ------------
    If you want to zip the files in a dataset, do the following:

        >>> ds.zip()


    """
    self._zip = True
    if session_info["lazy"] is False:
        self._execute = False
        self.run()
