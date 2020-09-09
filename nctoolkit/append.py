import os
import warnings


def append(self, x=None):
    """
    Add new file(s) to a dataset

    Parameters
    -------------
    x: str or list
     File path(s) to add to the dataset
    """

    # run any commands, as it makes no sense to add files while commands are waiting to run
    self.run()

    if x is None:
        raise TypeError("Please supply files")

    if type(x) is str:
        x = [x]
    len_x = len(x)

    x = list(set(x))

    if len(x) < len_x:
        warnings.warn("Duplicates removed from files")

    # check files are not already in the dataset

    if type(self.current) is list:
        check_list = self.current
    else:
        check_list = [self.current]

    for ff in x:
        if ff in check_list:
            raise ValueError(
                "You are trying to add a file that is already in the dataset"
            )

    for ff in x:
        if os.path.exists(ff) is False:
            raise ValueError(f"{ff} does not exist!")

    for ff in x:
        if type(self.current) is str:
            self.current = [self.current, ff]
        else:
            self.current.append(ff)
