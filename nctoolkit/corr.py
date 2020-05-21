
import copy

from nctoolkit.cleanup import cleanup, disk_clean
from nctoolkit.runthis import run_cdo, tidy_command
from nctoolkit.session import nc_safe
from nctoolkit.show import nc_variables
from nctoolkit.temp_file import temp_file


def cor(self, var1=None, var2=None, method="fld"):

    # Make sure variables are given
    if (var1 is None) or (var2 is None):
        raise ValueError("Both variables are not given")

    if type(var1) is not str:
        raise TypeError("var1 is not a str")

    if type(var2) is not str:
        raise TypeError("var2 is not a str")

    # this cannot be chained. So release
    self.run()

    # Check variables are in the dataset

    for ff in self:
        if var1 not in nc_variables(ff):
            raise ValueError(f"{var1} is not in the dataset")

        if var2 not in nc_variables(ff):
            raise ValueError(f"{var2} is not in the dataset")

    # Calculate the correlations in each file
    new_files = []
    new_commands = []

    for ff in self:

        # create the temp file for targeting
        target = temp_file(".nc")

        # create the cdo command and run it
        cdo_command = (
            f"cdo -{method}cor -selname,{var1} {ff} -selname,{var2} {ff} {target}"
        )
        cdo_command = tidy_command(cdo_command)
        target = run_cdo(cdo_command, target)

        new_files.append(target)
        new_commands.append(cdo_command)

    # update the state of the dataset
    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    # tidy up the attributes of the netcdf file in the dataset
    self.rename({var1: "cor"})
    self.set_units({"cor": "-"})
    self.set_longnames({"cor": f"Correlation between {var1} & {var2}"})

    cleanup()
    self.disk_clean()


def cor_space(self, var1=None, var2=None):
    """
    Calculate the correlation correct between two variables in space
    This is calculated for each time step. The correlation coefficient coefficient is calculated using values in all grid cells, ignoring missing values.

    Parameters
    -------------
    var1: str
        The first variable
    var2: str
        The second variable
    """

    cor(self, var1=var1, var2=var2, method="fld")


def cor_time(self, var1=None, var2=None):
    """
    Calculate the correlation correct in time between two variables
    The correlation is calculated for each grid cell, ignoring missing values.

    Parameters
    -------------
    var1: str
        The first variable
    var2: str
        The second variable
    """
    cor(self, var1=var1, var2=var2, method="tim")
