import inspect
import numpy as np

from nctoolkit.runthis import run_this

funs = ["abs", "floor", "ceil", "float", "int", "nint", "sqr",
"sqrt", "exp", "log10", "sin", "cos", "tan", "asin", "acos", "atan"]

translation = dict()
for ff in funs:
    if ff  in dir(np):
        translation[ff] = ff
translation["asin"] = "arcsin"
translation["acos"] = "arccos"
translation["atan"] = "arctan"

# translate the spatials
translation["spatial_mean"] = "fldmean"
translation["spatial_min"] = "fldmin"
translation["spatial_max"] = "fldmax"
translation["spatial_sum"] = "fldsum"


# translate the spatials
translation["vertical_mean"] = "vertmean"
translation["vertical_min"] = "vertmin"
translation["vertical_max"] = "vertmax"
translation["vertical_sum"] = "vertsum"


translation["zonal_mean"] = "zonmean"
translation["zonal_min"] = "zonmin"
translation["zonal_max"] = "zonmax"
translation["zonal_sum"] = "zonsum"
translation["isnan"] = "isMissval"

translation["cell_area"] = "gridarea"

translation["level"] = "clev"

translation["log"] = "ln"

translation["time_step"] = "ctimestep"

translation["year"] = "cyear"
translation["month"] = "cmonth"
translation["day"] = "cday"
translation["hour"] = "chour"
translation["second"] = "csecond"
translation["minute"] = "cminute"

translation["lon"] = "clon"
translation["lat"] = "clat"

translation["longitude"] = "clon"
translation["latitude"] = "clat"


# todo
# ensure methods work with all logical operators.
# convert code for fixing expression to a function. Invitation to bugs currently

import re
import inspect

# split using all possible mathematical operators
def split1(mystr):
    return re.split("([+-/*()<=])", mystr)

def split2(mystr):
    return re.split("([+-/*()<=:])", mystr)

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

    start = re.sub(" +", " ", " ".join(split1(start)).replace(" . ", "."))

    if "[" in start or "]" in start:
        raise ValueError("assign cannot accept [ or ]")

    if "{" in start or "}" in start:
        raise ValueError("assign cannot accept { or }")

    pattern1 = re.compile(",\s+\w+ = lambda")

    for x in pattern1.finditer(start):
        index = x.span()[0]
        start = start[:index] + ";" + start[index + 1:]


    if "||" in start:
        raise ValueError("|| is not valid syntax. Please use |!")

    if "&&" in start:
        raise ValueError("&& is not valid syntax. Please use &!")

    if "^" in start:
        raise ValueError("^ is not valid syntax. Please use **")

    start = start.replace("|", "||")
    start = start.replace("&", "&&")
    start = start.replace("**", "^")


    # we need to be able to identify lambdas and get rid of them
    #start = start.replace("=", "= ")
    start = re.sub(" +", " ", " ".join(split1(start)).replace(" . ", "."))

    # x. terms are from the netcdf file, not locally
    #a_list = []
    #for x in start.split(","):
    #    match1 = list(pattern.findall(x))[0]
    #    match2 = list(pattern.findall(x))[0][1:] + "."
    #    a_list.append(x.replace(match1, "").replace(match2, ""))
    #start = ",".join(a_list)


    # We now need to tidy up each element

    start = start.replace("=", " = ")
    new_start = []

    start = re.sub(" +", " ", " ".join(split1(start)).replace(" . ", "."))

    for ss in start.split(";"):
        x1 = split2(ss)
        x1 = [x.strip() for x in x1]
        ss_sub = ""
        for i in range(0, len(x1)):
            i_part = x1[i]
            if i > 0:
                if i < (len(x1)-1):
                    if x1[i+1] != "(" and x1[i].isidentifier() and (x1[i].isnumeric() == False) and x1[i+1] != ".":
                        if i > 1 and x1[i-1] != ".":
                            if x1[i] not in  frame.f_back.f_locals:
                                raise ValueError(f"{x1[i]} does not exist!")
                            i_part = frame.f_back.f_locals[x1[i]]
                            if type(i_part) not in [float,int]:
                                raise ValueError(f"{x1[i]} is not numeric!")
                            i_part = str(i_part)
                        if i == 0:
                            if x1[i] not in  frame.f_back.f_locals:
                                raise ValueError(f"{x1[i]} does not exist!")
                            i_part = frame.f_back.f_locals[x1[i]]
                            if type(i_part) not in [float,int]:
                                raise ValueError(f"{x1[i]} is not numeric!")
                            i_part = str(i_part)

                else:
                    if x1[i].isidentifier() and (x1[i].isnumeric() == False):
                        if x1[i-1] != ".":
                            i_part = frame.f_back.f_locals[x1[i]]
                            if type(i_part) not in [float,int]:
                                raise ValueError(f"{x1[i]} is not numeric!")
                            i_part = str(i_part)

            ss_sub+=i_part

        ss_sub = "".join(ss_sub)

        new_start.append(ss_sub)

    start = ";".join(new_start)

    start = " ".join(split1(start))

    new_start = []
    for tt in start.split(";"):

        tt_frag = []
        l_pattern = re.compile("lambda (\w*):")
        l_string = l_pattern.findall(tt)[0]
        tt1 = tt.replace(f"lambda {l_string}:", " ")
        tt1 = re.sub(" ", "",  tt1)
        tt1 = " ".join(split1(tt1)).replace(" . ", ".")
        tt1 = re.sub(" +", " ",  tt1)

        for ss in tt1.split(" "):
            if ss.startswith(f"{l_string}."):
                tt_frag.append(ss.replace(f"{l_string}.", ""))
            else:
                tt_frag.append(ss)

        tt_frag = " ".join(tt_frag)
        new_start.append(tt_frag)

    start = ";".join(new_start)
    start = " ".join(split1(start))

    start = start.replace(" lambda ", " ").replace(" ", "")


    for x in re.findall(r'\((.*?)\)',start):
        if x == "":
            raise ValueError("Please provide arguments to all functions!")

    del frame



    pattern = re.compile("\w*\\(")
    for x in pattern.findall(start):
        x_fixed = x.replace("(", "")
        if x_fixed == "pow":
            raise ValueError("pow is not available. Use ^ instead.")
        if x_fixed.strip() != "":
            if x_fixed not in translation.keys():
                raise ValueError(f"{x_fixed} is not a valid function!")

    # We need to fix pow functions potentially. Though, it might be better to stick with ^

    # translate numpy style functions to cdo functions
    for key in translation:
        start = start.replace(f"{key}(", f"{translation[key]}(")


    pattern = re.compile("\w*\\(+\w*\\)")
    for x in pattern.findall(start):
        if (len(re.findall(r"\(([A-Za-z0-9_]+)\)", x))) == 0:
            raise ValueError("Ensure all functions have arguments")

    def new_split(mystr):
        return re.split("([+-/*()&|<=])", mystr)

    for x in start.split(";"):
        y = " ".join(new_split(x))
        z = y.split(" = ")[1]
        total = 0
        for w in (z.replace(" (", "(")).split(" "):
            if w.strip().isidentifier():
                total+=1
        if total  == 0:
            raise ValueError("Formula does not use any dataset variables!")




    #return start

    # not sure what to do, if for example x[1] is an argument. Throw an error!


    # Finally, check functions are valid


    # create the cdo call and run it
    cdo_command = f"cdo -aexpr,'{start}'"
    run_this(cdo_command, self, output="ensemble")

