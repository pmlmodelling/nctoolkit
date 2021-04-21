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

