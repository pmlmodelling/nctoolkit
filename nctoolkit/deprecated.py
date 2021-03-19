import copy
import subprocess

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_this, run_nco, tidy_command, run_cdo
from nctoolkit.temp_file import temp_file
from nctoolkit.session import nc_safe, remove_safe
from nctoolkit.verticals import *
from nctoolkit.show import nc_variables
import warnings
import inspect


#####################################################
# Delete these in April 2021
#####################################################


def cell_areas(self, join=True):
    """
    Calculate the area of grid cells.
    Area of grid cells is given in square meters.

    Parameters
    -------------
    join: boolean
        Set to False if you only want the cell areas to be in the output.
        join=True adds the areas as a variable to the dataset. Defaults to True.
    """
    warnings.warn(message="Warning: cell_areas is deprecated. Use cell_area!")

    if isinstance(join, bool) is False:
        raise TypeError("join is not boolean")

    # release if you need to join the cell areas to the original file
    if join:
        self.run()

    # get the cdo version
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    cdo_version = cdo_check.split("(")[0].strip().split(" ")[-1]

    # first run the join case
    if join:

        new_files = []
        new_commands = []

        for ff in self:

            if cdo_version in ["1.9.3", "1.9.4", "1.9.5", "1.9.6"]:

                # in cdo < 1.9.6 chaining doesn't work with merge

                if "cell_area" in nc_variables(ff):
                    raise ValueError("cell_area is already a variable")

                target1 = temp_file(".nc")

                cdo_command = f"cdo -gridarea {ff} {target1}"
                cdo_command = tidy_command(cdo_command)
                target1 = run_cdo(cdo_command, target1)
                new_files.append(target1)
                new_commands.append(cdo_command)

                target = temp_file(".nc")

                cdo_command = f"cdo -merge {ff} {target1} {target}"
                cdo_command = tidy_command(cdo_command)
                target = run_cdo(cdo_command, target)
                new_files.append(target)

                new_commands.append(cdo_command)

            else:

                if "cell_area" in nc_variables(ff):
                    raise ValueError("cell_area is already a variable")

                target = temp_file(".nc")

                cdo_command = f"cdo -merge {ff} -gridarea {ff} {target}"
                cdo_command = tidy_command(cdo_command)
                target = run_cdo(cdo_command, target)
                new_files.append(target)

                new_commands.append(cdo_command)

        for x in new_commands:
            self.history.append(x)

        self.current = new_files

        for ff in new_files:
            remove_safe(ff)

        self._hold_history = copy.deepcopy(self.history)

        cleanup()

    else:

        cdo_command = "cdo -gridarea"
        run_this(cdo_command, self, output="ensemble")

    # add units

    self.set_units({"cell_area": "m^2"})

    if join:
        self.run()
        self.disk_clean()


def remove_variables(self, vars=None):
    """
    Remove variables
    This will remove stated variables from files in the dataset.

    Parameters
    -------------
    vars : str or list
        Variable or variables to be removed from the dataset.
        Variables that are listed but not in the dataset will be ignored
    """
    warnings.warn(message="Warning: remove_variables is deprecated. Use drop!")

    # Some checks on the validity of variables supplied
    if vars is None:
        raise ValueError("Please supplied vars")

    if type(vars) is not list:
        vars = [vars]

    for vv in vars:
        if type(vv) is not str:
            raise TypeError(f"{vv} is not a str")

    vars = str_flatten(vars, ",")

    # create the cdo command and run it
    cdo_command = f"cdo -delete,name={vars}"
    run_this(cdo_command, self, output="ensemble")




# todo
# ensure methods work with all logical operators.
# convert code for fixing expression to a function. Invitation to bugs currently


def fix_expression(operations=None, i_frame=None):

    if type(operations) is not dict:
        raise TypeError("No expression was provided")

    # first,we need to convert the operations dictionary to a cdo expression

    expr = []

    for key, value in operations.items():

        if type(key) is not str:
            raise TypeError(f"{key} is not a str")
        if type(value) is not str:
            raise TypeError(f"{value} is not a str")

        for x in ["&&", "||"]:
            if x in value:
                raise ValueError("Invalid expression provided")

        new_x = (
            "".join((" {} ".format(el) if el in "=><+-/*^()&" else el for el in value))
            .replace(" &  & ", " && ")
            .replace(" & ", " && ")
        )
        new_x = new_x.replace(" | ", " || ")
        expr_split = new_x.split(" ")
        new_expr = ""

        for x in expr_split:
            if x.startswith("@"):
                # We need to first check the local variable supplied is a numeric
                if x.replace("@", "") in i_frame.f_back.f_locals:
                    new_x = i_frame.f_back.f_locals[x.replace("@", "")]
                else:
                    raise ValueError(
                        str(x.replace("@", "")) + " is not a local variable"
                    )

                if isinstance(new_x, (int, float)) is False:
                    raise TypeError(x + " is not numeric!")
                new_expr += str(new_x)
            else:
                new_expr += x

        expr.append(key + "=" + new_expr)

    expr = ";".join(expr)
    expr = expr.replace(" ", "")
    expr = '"' + expr + '"'

    return expr


def mutate(self, operations=None):
    """
    Create new variables using mathematical expressions, and keep original variables

    Parameters
    -------------
    operations : dict
        operations to apply. The keys are the new variables to generate.
        The values are the mathematical operations to carry out. Both must be strings.
    """
    warnings.warn(message="Warning: mutate is deprecated. Use assign!")

    if type(operations) is not dict:
        raise TypeError("No expression was provided")

    frame = inspect.currentframe()

    try:
        expr = fix_expression(operations, i_frame=frame)
    finally:
        del frame
    # create the cdo call and run it
    cdo_command = f"cdo -aexpr,{expr}"
    run_this(cdo_command, self, output="ensemble")


def transmute(self, operations=None):
    """
    Create new variables using mathematical expressions, and drop original variables

    Parameters
    -------------
    operations : dict
        operations to apply. The keys are the new variables to generate.
        The values are the mathematical operations to carry out. Both must be strings.
    """
    warnings.warn(message="Warning: transmute is deprecated. Use assign!")
    # create the cdo call and run it

    frame = inspect.currentframe()

    try:
        expr = fix_expression(operations, i_frame=frame)
    finally:
        del frame
    # create the cdo call and run it
    cdo_command = "cdo -expr," + expr
    run_this(cdo_command, self, output="ensemble")

