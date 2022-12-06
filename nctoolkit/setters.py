import copy
import warnings

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_this, run_nco
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe
from nctoolkit.show import nc_variables
from nctoolkit.utils import name_check


def set_year(self, x):
    """
    Set the year in a dataset

    Parameters
    -------------
    x : int
        Year to set dataset to
    """

    if not isinstance(x, int):
        raise ValueError(f"{x} is not a int")
    cdo_command = f"cdo -setyear,{x}"
    run_this(cdo_command, self, output="ensemble")

def set_day(self, x):
    """
    Set the day for each time step in a dataset

    Parameters
    -------------
    x : int
        Day to set dataset to
    """

    if not isinstance(x, int):
        raise ValueError(f"{x} is not a int")
    cdo_command = f"cdo -setday,{x}"
    run_this(cdo_command, self, output="ensemble")



def set_precision(self, x):
    """
    Set the precision in a dataset

    Parameters
    -------------
    x : str
        The precision. One of 'I8', 'I16', 'I32', 'F32', 'F64'.
    month : int
        The month
    day : int
        The day
    base_year : int
        The base year for time creation in the netCDF. Defaults to 1900.
    """

    if x not in ["I8", "I16", "I32", "F32", "F64"]:
        raise ValueError(f"{x} is not a valid precision")

    self._precision = x


def set_date(self, year=None, month=None, day=None, base_year=1900):
    """
    Set the date in a dataset
    You should only do this if you have to fix/change a dataset with a single,
    not multiple dates.

    Parameters
    -------------
    year : int
        The year
    month : int
        The month
    day : int
        The day
    base_year : int
        The base year for time creation in the netCDF. Defaults to 1900.
    """

    if year is None:
        raise ValueError("Please supply a year")

    if month is None:
        raise ValueError("Please supply a month")

    if day is None:
        raise ValueError("Please supply a day")

    if not isinstance(year, int):
        try:
            year = int(year)
        except:
            raise TypeError("Unable to coerce year to int")

    if not isinstance(month, int):
        try:
            month = int(month)
        except:
            raise TypeError("Unable to coerce month to int")

    if not isinstance(day, int):
        try:
            day = int(day)
        except:
            raise TypeError("Unable to coerce day to int")

    # check that the values supplied are valid
    # This will convert things to ints, and if it can't be done, throw an error
    if not isinstance(year, int):
        raise TypeError("year supplied is not an int")
    if not isinstance(month, int):
        raise TypeError("month supplied is not an int")
    if not isinstance(day, int):
        raise TypeError("day supplied is not an int")

    cdo_command = (
        f"cdo -setreftime,{str(base_year)}-01-01 "
        f"-setdate,{str(year)}-{str(month)}-{str(day)}"
    )

    run_this(cdo_command, self, output="ensemble")

def missing_as(self, value=None):
    """
    Convert missing values to a constant

    Parameters
    -------------
    value : Number to convert the missing values to
        If int/float is provided, the missing value will be converted to that.
    """

    try:
        test = float(value)
    except:
        raise TypeError("value must be coercible to float")

    cdo_command = f"cdo -setmisstoc,{value}"

    run_this(cdo_command, self, output="ensemble")

def set_fill(self, value=None):
    """
    Set the fill value 

    Parameters
    -------------
    value : 2 variable list or int/float
        If int/float is provided, the missing value will be set to that.
        If a list is provided, values between the two values (inclusive)
        of the list are set to missing.
    """

    if value is None:
        raise ValueError("Please supply missing value")

    try:
        test = float(value)
    except:
        raise TypeError("value cannot evaluate to a float")

    cdo_command = f"cdo -setmissval,{value} -setmissval,nan" 

    run_this(cdo_command, self, output="ensemble")


def as_missing(self, value=None):
    """
    Change a range or individual value to missing.

    Parameters
    -------------
    value : 2 variable list or int/float
        If int/float is provided, the missing value will be set to that.
        If a list is provided, values between the two values (inclusive)
        of the list are set to missing.
    """

    if value is None:
        raise ValueError("Please supply missing value")

    if isinstance(value, (int, float)):
        value = [value, value]

    if not isinstance(value, list):
        raise TypeError("Please supply a list, int or float!")

    for vv in value:
        if not isinstance(vv, (int, float)):
            raise TypeError(f"{vv} is not an int or float")

    if isinstance(value, list):
        cdo_command = f"cdo -setrtomiss,{str(value[0])},{str(value[1])}"

    run_this(cdo_command, self, output="ensemble")


def set_units(self, unit_dict=None):
    """
    Set the units for variables

    Parameters
    -------------
    unit_dict : dict
        A dictionary where the key-value pairs are the variables and
        new units respectively.
    """

    if unit_dict is None:
        raise ValueError("Please supply unit_dict")

    # Check that a dictionary has been supplied
    if not isinstance(unit_dict, dict):
        raise TypeError("A dictionary has not been supplied!")

    for key, value in unit_dict.items():
        if name_check(key) is False:
            raise ValueError(f"{key} is not a valid netCDF variable name")

    if len(self.history) == len(self._hold_history):
        variables = nc_variables(self[0])
        for key in unit_dict:
            if key not in variables:
                if len(self) > 1:
                    warnings.warn(message = f"{key} is not in the first file of the dataset")
                else:
                    warnings.warn(message = f"{key} is not in the dataset")

    # change the units in turn. This doesn't seem to be something you can chain?
    for i in unit_dict:
        if not isinstance(i, str):
            raise TypeError("key,values in unit_dict are not strings")
        if not isinstance(unit_dict[i], str):
            raise TypeError("key,values in unit_dict are not strings")

        cdo_command = f'cdo -setattribute,{i}@units="{unit_dict[i]}"'
        run_this(cdo_command, self, output="ensemble")


def set_longnames(self, name_dict=None):
    """
    Set the long names of variables

    Parameters
    -------------
    name_dict : dict
        Dictionary with key, value pairs representing the variable names and
        their long names

    """
    if name_dict is None:
        raise ValueError("Please supply name_dict")

    if not isinstance(name_dict, dict):
        raise TypeError("Please supply a dictionary")

    self.run()

    if not isinstance(name_dict, dict):
        TypeError("A dictionary has not been supplied!")

    # change the units in turn. This doesn't seem to be something you can chain?

    new_commands = []
    new_files = []

    if len(self.history) == len(self._hold_history):
        variables = nc_variables(self[0])
        for key in name_dict:
            if key not in variables:
                if len(self) > 1:
                    warnings.warn(message = f"{key} is not in the first file of the dataset")
                else:
                    warnings.warn(message = f"{key} is not in the dataset")

    for key, value in name_dict.items():
        if name_check(key) is False:
            raise ValueError(f"{key} is not a valid netCDF variable name")

    for ff in self:
        nco_command = "ncatted "
        for i in name_dict:
            if not isinstance(i, str):
                raise TypeError("key,values in name_dict are not strings")
            if not isinstance(name_dict[i], str):
                raise TypeError("key,values in name_dict are not strings")
            i_dict = name_dict[i]
            i_dict = i_dict.replace('"', "'")
            nco_command += "-a long_name," + i + ',o,c,"' + i_dict + '" '

        target = temp_file("nc")

        nco_command += ff + " " + target

        target = run_nco(nco_command, target)

        new_files.append(target)
        new_commands.append(nco_command)

    self.history += new_commands
    self._hold_history = copy.deepcopy(self.history)

    self.current = new_files

    for ff in new_files:
        remove_safe(ff)

    # clean up the directory
    cleanup()
    self.disk_clean()
