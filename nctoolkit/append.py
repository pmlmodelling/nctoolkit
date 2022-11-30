import os
import warnings
from nctoolkit.session import append_safe, remove_safe
import nctoolkit.api as api


def append(self, x=None):
    """
    Add new file(s) to a dataset.

    Parameters
    -------------
    x: str or list
     File path(s) to add to the dataset


    Examples
    ------------
    If you want to add a dataset ds2 to another dataset ds1, do the following:

    >>> ds1.append(ds2)

    If you want to add a new file to a dataset, do this:

    >>> ds.append("infile.nc")


    """

    # run, as it makes no sense to add files while commands are waiting to run
    self.run()
    if isinstance(x, api.DataSet):
        x.run()

    if x is None:
        raise TypeError("Please supply files")

    if isinstance(x, str):
        x = [x]
    len_x = len(x)

    x = list(set(x))

    if len(x) < len_x:
        warnings.warn("Duplicates removed from files")

    # check files are not already in the dataset

    check_list = self.current

    for ff in x:
        if ff in check_list:
            warnings.warn(
                "You are trying to add a file that is already in the dataset"
            )

    for ff in x:
        if os.path.exists(ff) is False:
            raise ValueError(f"{ff} does not exist!")

    for ff in x:
        append_safe(ff)
        self.current.append(ff)


def remove(self, x=None):
    """
    Remove file(s) from a dataset

    Parameters
    -------------
    x: str or list
     File path(s) to remove from a dataset

    Examples
    ------------
    If you want to remove a file from a dataset do the following:

    >>> ds.remove("infile.nc")

    """

    if x is None:
        raise ValueError("Please provide files to remove!")

    if isinstance(x, str):
        x = [x]

    for ff in x:
        if ff not in self:
            raise ValueError(f"{x} is not a member of the dataset!")

    for ff in x:
        self.current.remove(ff)
        remove_safe(ff)
