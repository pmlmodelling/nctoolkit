import inspect
import numpy as np
from nctoolkit.flatten import str_flatten

from nctoolkit.runthis import run_this


def between_brackets(s):
    return s[s.find("(") + 1 : s.find(")")]


def find_parens(s):
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == "[":
            pstack.append(i)
        elif c == "]":
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i

    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))

    return toret


def find_parens2(s):
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == "{":
            pstack.append(i)
        elif c == "}":
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i

    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))

    return toret


def find_parens3(s):
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == "(":
            pstack.append(i)
        elif c == ")":
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i

    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))

    return toret


funs = [
    "abs",
    "floor",
    "ceil",
    "float",
    "int",
    "nint",
    "sqr",
    "sqrt",
    "exp",
    "log10",
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
]

translation = dict()
for ff in funs:
    if ff in dir(np):
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
    LAMBDA = lambda: 0
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
    start = inspect.getsourcelines(start)[0][0].replace("\n", "")
    start = start[start.find("(") + 1 :-1]

    pattern1 = re.compile(",\s+\w+ = lambda")

    for x in pattern1.finditer(start):
        index = x.span()[0]
        start = start[:index] + ";" + start[index + 1 :]


    command = list()
    starts = start
    for start in starts.split(";"):

        # pattern1 = re.compile("\w*\[\w*\]")
        # pattern1 = re.compile("\w*\.\w*\[\w*\]")
        # if len(pattern1.findall(start)) > 0:
        #    for x in pattern1.findall(start):
        #        raise ValueError(f"The following are not available: {x}. Use local variables")

        # extract x[1] etc. terms
        # pattern1 = re.compile("[a-zA-Z]\w*\[([A-Za-z0-9_.]+)\]")

        # terms = re.finditer(r"[a-zA-Z]\w*\[([A-Za-z0-9_.\+\*\-\/]+)\]", start)
        # terms = [x[0] for x in list(terms)]

        # for x in terms:
        #    try:
        #        new_term = (eval(x, globals(),  frame.f_back.f_locals))
        #    except:
        #        raise ValueError(f"{x} is not available!")

        #    start = start.replace(x, str(new_term))

        patternl = re.compile("lambda \w*:")
        lambda_value = patternl.findall(start)[0][-2]

        start = (
            " ".join(split1(start))
            .replace("  ", " ")
            .replace(" ( ", "(")
            .replace(" . ", ".")
        )

        # run equations first.
        # key here is that equation can only pure pure python or pure cdo

        while True:
            check_start = start
            pars = find_parens(start)
            for key in pars:
                old_start = start
                start = (
                    start[:key]
                    + start[key : (pars[key] + 1)].replace(" ", "")
                    + start[pars[key] + 1 :]
                )
                if start != old_start:
                    break
            if check_start == start:
                break

        while True:
            check_start = start
            pars = find_parens2(start)
            for key in pars:
                old_start = start
                start = (
                    start[:key]
                    + start[key : (pars[key] + 1)].replace(" ", "")
                    + start[pars[key] + 1 :]
                )
                if start != old_start:
                    break
            if check_start == start:
                break

        start = start.replace(";", " ; ").replace("  ", " ")

        # tidy functions

        terms = list(
            set(
                [
                    x
                    for x in " ".join(split1(start))
                    .replace(" (", "(")
                    .replace(" . ", ".")
                    .split(" ")
                    if x.endswith("(") and len(x) > 1
                ]
            )
        )


        for x in terms:
            if ("[" in x and f"{lambda_value}." in x) == False:
                for y in re.finditer(x.replace("(", "\\(").replace("[", "\\["), start):
                    old_start = start
                    start_parens = find_parens3(start)
                    x_term = x + start[y.span()[1] : start_parens[y.span()[1] - 1] + 1]
                    start = start.replace(x_term, x_term.replace(" ", ""))

        start = start.replace(" [", "[")

        error_message = None
        for x in start.split(" "):
            if "(" in x:
                x_fun = x.split("(")[0]
                pattern1 = re.compile("[A-Za-z\\.\\_]*")
                if pattern1.findall(x_fun)[0] == x_fun:
                    try:
                        # need to tweak this so that it captures the output and returns an appropriate error
                        if eval(f"callable({x_fun})", globals(), frame.f_back.f_locals):
                            error_message = f"{x} does not evaluate to numeric!"
                            new_x = eval(x, globals(), frame.f_back.f_locals)
                            if "float" not in str(type(new_x)) and "int" not in str(
                                type(new_x)
                            ):
                                error_message = f"{x} does not evaluate to numeric!"

                            new_start = ""
                            for y in start.split(" "):
                                if y != x:
                                    new_start += " " + y
                                else:
                                    new_start += " " + str(new_x)
                            start = new_start
                            error_message = None

                    except:

                        x_term = between_brackets(x)
                        #if x_fun in translation.keys():
                        #    error_message = f"{x} cannot be evaluated to numeric!"
                        if x_fun in translation.keys():
                            if f"{lambda_value}." in x_term == False:
                                raise ValueError(f"Error for {x}: nctoolkit functions must take dataset variables as args!")
            if error_message is not None:
                break

        if error_message is not None:
            raise ValueError(error_message)

        start = (
            " ".join(split1(start))
            .replace("  ", " ")
            .replace(" ( ", "(")
            .replace(" . ", ".")
        )

        # run equations first.
        # key here is that equation can only pure pure python or pure cdo

        while True:
            check_start = start
            pars = find_parens(start)
            for key in pars:
                old_start = start
                start = (
                    start[:key]
                    + start[key : (pars[key] + 1)].replace(" ", "")
                    + start[pars[key] + 1 :]
                )
                if start != old_start:
                    break
            if check_start == start:
                break

        while True:
            check_start = start
            pars = find_parens2(start)
            for key in pars:
                old_start = start
                start = (
                    start[:key]
                    + start[key : (pars[key] + 1)].replace(" ", "")
                    + start[pars[key] + 1 :]
                )
                if start != old_start:
                    break
            if check_start == start:
                break

        start = start.replace(";", " ; ").replace("  ", " ")

        terms = (
            start.replace(" . ", ".")
            .replace(") ", ")")
            .replace(") ", ")")
            .replace("  ", " ")
            .split(" ")
        )

        for x in terms:
            if "[" in x:
                if f"{lambda_value}." in x:
                    raise ValueError(f"{x} is not valid syntax")
                try:
                    new_term = eval(x, globals(), frame.f_back.f_locals)
                except:
                    raise ValueError(f"{x} is not available!")
                if "float" not in str(type(new_term)) and "int" not in str(
                    type(new_term)
                ):
                    raise ValueError(f"{x} does not evaluate to numeric!")

                new_start = ""
                for y in start.split(" "):
                    if y != x:
                        new_start += " " + y
                    else:
                        new_start += " " + str(new_term)
                start = new_start

        terms = start.split(" ")

        for x in terms:
            if "{" in x:
                if f"{lambda_value}." in x:
                    raise ValueError(f"{x} is not valid syntax")
                try:
                    new_term = eval(x, globals(), frame.f_back.f_locals)
                except:
                    raise ValueError(f"{x} is not available!")
                if "float" not in str(type(new_term)) and "int" not in str(
                    type(new_term)
                ):
                    raise ValueError(f"{x} does not evaluate to numeric!")

                new_start = ""
                for y in start.split(" "):
                    if y != x:
                        new_start += " " + y
                    else:
                        new_start += " " + str(new_term)
                start = new_start

        # fix powers

        if "^" in start:
            raise ValueError("^ is not valid syntax. Please use **")
        start = start.replace("* ", "*").replace("**", "^")

        start = re.sub(" +", " ", " ".join(split1(start)).replace(" . ", "."))

        # if "{" in start or "}" in start:
        #    raise ValueError("assign cannot accept { or }")

        pattern1 = re.compile(",\s+\w+ = lambda")

        for x in pattern1.finditer(start):
            index = x.span()[0]
            start = start[:index] + ";" + start[index + 1 :]

        if "||" in start:
            raise ValueError("|| is not valid syntax. Please use |!")

        if "&&" in start:
            raise ValueError("&& is not valid syntax. Please use &!")

        start = start.replace("|", "||")
        start = start.replace("&", "&&")

        # we need to be able to identify lambdas and get rid of them
        # start = start.replace("=", "= ")
        start = re.sub(" +", " ", " ".join(split1(start)).replace(" . ", "."))

        # x. terms are from the netcdf file, not locally
        # a_list = []
        # for x in start.split(","):
        #    match1 = list(pattern.findall(x))[0]
        #    match2 = list(pattern.findall(x))[0][1:] + "."
        #    a_list.append(x.replace(match1, "").replace(match2, ""))
        # start = ",".join(a_list)

        # We now need to tidy up each element


        start = " ".join(split1(start))
        start = start.replace("  ", " ")
        start = start.replace(" (", "(").replace(" . ", ".")
        terms = start.split(" ")

        error_message = None
        for i in range(2, len(terms)):
            if (
                terms[i].isidentifier()
                and terms[i - 2] != ";"
                and terms[i] != "lambda"
                and terms[i + 1] != lambda_value
            ):
                term = terms[i]
                if term in frame.f_back.f_locals:
                    try:
                        new_term = eval(term, globals(), frame.f_back.f_locals)
                        if type(new_term) not in [int, float]:
                            error_message = f"{term} does not evaluate to a numeric!"
                        new_start = ""
                        for y in start.split(" "):
                            if y != term:
                                new_start += " " + y
                            else:
                                new_start += " " + str(new_term)
                        start = new_start
                    except:
                        raise ValueError(f"{term} is not available!")
                else:
                    raise ValueError(f"{term} is not available!")

        if error_message is not None:
            raise ValueError(error_message)

        if False:
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
                        if i < (len(x1) - 1):
                            if (
                                x1[i + 1] != "("
                                and x1[i].isidentifier()
                                and (x1[i].isnumeric() == False)
                                and x1[i + 1] != "."
                            ):
                                if i > 1 and x1[i - 1] != ".":
                                    if x1[i] not in frame.f_back.f_locals:
                                        raise ValueError(f"{x1[i]} does not exist!")
                                    i_part = frame.f_back.f_locals[x1[i]]
                                    if type(i_part) not in [float, int]:
                                        raise ValueError(f"{x1[i]} is not numeric!")
                                    i_part = str(i_part)
                                if i == 0:
                                    if x1[i] not in frame.f_back.f_locals:
                                        raise ValueError(f"{x1[i]} does not exist!")
                                    i_part = frame.f_back.f_locals[x1[i]]
                                    if type(i_part) not in [float, int]:
                                        raise ValueError(f"{x1[i]} is not numeric!")
                                    i_part = str(i_part)

                        else:
                            if x1[i].isidentifier() and (x1[i].isnumeric() == False):
                                if x1[i - 1] != ".":
                                    i_part = frame.f_back.f_locals[x1[i]]
                                    if type(i_part) not in [float, int]:
                                        raise ValueError(f"{x1[i]} is not numeric!")
                                    i_part = str(i_part)

                    ss_sub += i_part

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
            tt1 = re.sub(" ", "", tt1)
            tt1 = " ".join(split1(tt1)).replace(" . ", ".")
            tt1 = re.sub(" +", " ", tt1)

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

        for x in re.findall(r"\((.*?)\)", start):
            if x == "":
                raise ValueError("Please provide arguments to all functions!")

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


        start = " ".join(split1(start))
        def new_split(mystr):
            return re.split("([+-/*()&|<=^])", mystr)

        for x in start.split(";"):
            y = " ".join(new_split(x))
            z = y.split(" = ")[1]
            total = 0
            for w in (z.replace(" (", "(")).split(" "):
                if w.strip().isidentifier():
                    total += 1
            if total == 0:
                raise ValueError("Formula does not use any dataset variables!")

        command.append(start)

        # Now evaluate any

    command = ";".join(command)

    command = " ".join(split1(command)).replace(" . ", ".").replace(";", " ; ")


    for term in command.split(" "):

        if "." in term:
            pattern1 = re.compile("[a-zA-Z]")
            if len(pattern1.findall(term)) > 0:
                if term.split(".")[0] in frame.f_back.f_locals:
                    try:
                        new_term = eval(term, globals(), frame.f_back.f_locals)
                        new_start = ""
                        for y in command.split(" "):
                            if y != term:
                                new_start += " " + y
                            else:
                                new_start += " " + str(new_term)
                        command = new_start
                    except:
                        raise ValueError(f"{term} is not available!")
                else:
                    raise ValueError(f"{term} is not available!")

    command = command.replace(" ", "")

    del frame

    # return start

    # create the cdo call and run it
    cdo_command = f"cdo -aexpr,'{command}'"
    run_this(cdo_command, self, output="ensemble")
