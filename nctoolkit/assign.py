import inspect

from nctoolkit.runthis import run_this


# todo
# ensure methods work with all logical operators.
# convert code for fixing expression to a function. Invitation to bugs currently

import re
import inspect

# split using all possible mathematical operators
def split1(mystr):
    return re.split("([+-/*()<=])", mystr)

def is_lambda(v):
  LAMBDA = lambda:0
  return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__
import inspect

pattern = re.compile(":\w*")


def assign(self, **kwargs):
    """
    Create new variables using mathematical expressions, and keep original variables

    Parameters
    -------------
    operations : dict
        operations to apply. The keys are the new variables to generate.
        The values are the mathematical operations to carry out. Both must be strings.
    """
    frame = inspect.currentframe()

    # first we need to check if everything is a lambda function
    for yy in kwargs:
        if is_lambda(kwargs[yy]) == False:
            raise ValueError("Please check everything is a lambda function!")

    # now, we need to parse things.

    start = kwargs[yy]
    start =  inspect.getsourcelines(start)[0][0].replace("\n", "")[:-1]
    start = start[start.find("(")+1:]

    # we need to be able to identify lambdas and get rid of them
    start = start.replace("=", "= ")
    start = start.replace(" lambda ", " ").replace(" ", "")

    # x. terms are from the netcdf file, not locally
    a_list = []
    for x in start.split(","):
        match1 = list(pattern.findall(x))[0]
        match2 = list(pattern.findall(x))[0][1:] + "."
        a_list.append(x.replace(match1, "").replace(match2, ""))
    start = ",".join(a_list)


    # We now need to tidy up each element

    start = start.replace("=", " = ")
    new_start = ""

    x1 = split1(start)

    new_start = ""
    for i in range(0, len(x1)):
        i_part = x1[i]
        if i < (len(x1)-1):
            if x1[i+1] != "(" and x1[i].isalnum() and (x1[i].isnumeric() == False):
                i_part = str(frame.f_back.f_locals[x1[i]])
        else:
            if x1[i].isalnum() and (x1[i].isnumeric() == False):
                i_part = str(frame.f_back.f_locals[x1[i]])

        new_start+=i_part


    start = new_start.replace(" ", "")

    for x in re.findall(r'\((.*?)\)',start):
        if x == "":
            raise ValueError("Please provide arguments to all functions!")

    del frame
    #return start

    start = start.replace(",", ";")


    # create the cdo call and run it
    cdo_command = f"cdo -aexpr,'{start}'"
    run_this(cdo_command, self, output="ensemble")

