
import copy
import inspect

from nctoolkit.runthis import run_this


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

                if isinstance(new_x, (int, float)) == False:
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
        operations to apply. The keys are the new variables to generate. The values are the mathematical operations to carry out. Both must be strings.
    """

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
        operations to apply. The keys are the new variables to generate. The values are the mathematical operations to carry out. Both must be strings.
    """
    # create the cdo call and run it

    frame = inspect.currentframe()

    try:
        expr = fix_expression(operations, i_frame=frame)
    finally:
        del frame
    # create the cdo call and run it
    cdo_command = "cdo -expr," + expr
    run_this(cdo_command, self, output="ensemble")


def sum_all(self, drop=True):
    """
    Calculate the sum of all variables for each time step

    Parameters
    -------------
    drop : boolean
        Do you want to keep variables?
    """

    self.run()

    if (type(self.current) is list) and (self._merged == False):
        raise TypeError("This only works for single files presently")

    if drop == True:
        self.transmute({"total": "+".join(self.variables)})

    else:
        if "total" not in self.variables:
            self.mutate({"total": "+".join(self.variables)})
        else:
            i = 0
            while True:
                if f"total{i}" not in self.variables:
                    break
                i += 1
            self.mutate({"total" + str(i): "+".join(self.variables)})
