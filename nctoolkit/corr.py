import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_cdo, tidy_command
from nctoolkit.show import nc_variables
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe, get_safe


def cor(self, var1=None, var2=None, method="fld"):

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    # Make sure variables are given
    if (var1 is None) or (var2 is None):
        raise ValueError("Both variables are not given")

    if not isinstance(var1, str):
        raise TypeError("var1 is not a str")

    if not isinstance(var2, str):
        raise TypeError("var2 is not a str")

    # this cannot be chained. So release
    self.run()

    # Check variables are in the dataset

    for ff in self:
        if var1 not in nc_variables(ff):
            raise ValueError(f"{var1} is not in the dataset")

        if var2 not in nc_variables(ff):
            raise ValueError(f"{var2} is not in the dataset")

    if var1 != var2:
        contents = self.contents
        df = contents.query("variable in [@var1, @var2]").loc[:,["variable", "data_type"]]
        # if
        if len([x for x in df.index if "file" in str(x)]) == 0:
            df.index = ["file" for x in range(len(df.index))]
        df = (
            df
            .pivot(values = "data_type", columns = "variable")
            .rename(columns = {var1:"var1"})
            .rename(columns = {var2:"var2"})
        )
        if len(df.query("var1 != var2")) > 0:
            raise ValueError(f"{var1} and {var2} have different data types. Please select data type with set_precision. Suggestion: F32.")



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
        target = run_cdo(cdo_command, target, precision=self._precision)

        new_files.append(target)
        new_commands.append(cdo_command)

    # update the state of the dataset
    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    for ff in new_files:
        if len([x for x in get_safe() if x == ff]) > 1:
            remove_safe(ff)

    # tidy up the attributes of the netCDF file in the dataset
    self.rename({var1: "cor"})
    self.set_units({"cor": "-"})
    self.set_longnames({"cor": f"Correlation between {var1} & {var2}"})

    cleanup()
    self.disk_clean()


def cor_space(self, var1=None, var2=None):
    """
    Calculate the correlation correct between two variables in space
    This is calculated for each time step. The correlation coefficient coefficient is
    calculated using values in all grid cells, ignoring missing values.

    Parameters
    -------------
    var1: str
        The first variable
    var2: str
        The second variable

    Examples
    ------------

    If you wanted to calculate the spatial correlation coefficient between variables x and y in a dataset, you would do this:

    >>> ds.cor_space("x", "y")

    The correlation coefficient will be calculated for each time step.


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

    Examples
    ------------

    If you wanted to calculate the temporal correlation coefficient between variables x and y in a dataset, you would do this:

    >>> ds.cor_space("x", "y")

    The correlation coefficient will be calculated for each grid cell.  This method will indicate how temporally correlated variables are
    in different spatial regions.
    """
    cor(self, var1=var1, var2=var2, method="tim")
