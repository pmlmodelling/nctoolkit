from .runthis import run_this
import inspect


# todo
# ensure methods work with all logical operators.
# convert code for fixing expression to a function. Invitation to bugs currently


def transmute(self, operations = None):
    """
    Create new variables using mathematical expressions, and drop original variables

    Parameters
    -------------
    operations : dict
        operations to apply. The keys are the new variables to generate. The values are the mathematical operations to carry out.
    """

    if type(operations) is not dict:
        raise TypeError("No expression was provided")

    # first,we need to convert the operations dictionary to a cdo expression

    expr = []

    for key,value in operations.items():

        new_x = ''.join((' {} '.format(el) if el in '=><+-/*^()&' else el for el in value)).replace(" &  & ", " && ").replace(" & ", " && ")
        expr_split = new_x.split(" ")
        new_expr = ""

        for x in expr_split:
            if x.startswith("@"):
                # We need to first check the local variable supplied is a numeric
                if x.replace("@", "") in inspect.currentframe().f_back.f_locals:
                    new_x = inspect.currentframe().f_back.f_locals[x.replace("@", "")]
                else:
                    raise ValueError(str(x.replace("@", "")) + " is not a local variable")

                if isinstance(new_x, (int, float)) == False:
                    raise TypeError(x +  " is not numeric!")
                new_expr +=  str(new_x)
            else:
                new_expr +=  x

        expr.append(key + "=" + new_expr)

    expr = ";".join(expr)
    expr = expr.replace(" ", "" )
    expr = '"' + expr + '"'

    # create the cdo call and run it
    cdo_command = "cdo -expr," + expr
    run_this(cdo_command, self, output = "ensemble")

def mutate(self, operations = None):
    """
    Create new variables using mathematical expressions, and keep original variables

    Parameters
    -------------
    operations : dict
        operations to apply. The keys are the new variables to generate. The values are the mathematical operations to carry out.
    """

    # check operations is of valid type
    if type(operations) is not dict:
        raise TypeError("No expression was provided")

    # first,we need to convert the operations dictionary to a cdo expression

    expr = []

    for key,value in operations.items():

        new_x = ''.join((' {} '.format(el) if el in '=><+-/*^()&' else el for el in value)).replace(" &  & ", " && ").replace(" & ", " && ")
        #new_x = ''.join((' {} '.format(el) if el in '=><+-/*^()' else el for el in value))
        expr_split = new_x.split(" ")
        new_expr = ""

        for x in expr_split:
            if x.startswith("@"):
                # We need to first check the local variable supplied is a numeric
                if x.replace("@", "") in inspect.currentframe().f_back.f_locals:
                    new_x = inspect.currentframe().f_back.f_locals[x.replace("@", "")]
                else:
                    raise ValueError(str(x.replace("@", "")) + " is a local variable")

                if isinstance(new_x, (int, float)) == False:
                    raise TypeError(x +  " is not numeric!")
                new_expr +=  str(new_x)
            else:
                new_expr +=  x

        expr.append(key + "=" + new_expr)


    expr = ";".join(expr)
    expr = expr.replace(" ", "" )
    expr = '"' + expr + '"'

    # create the cdo call and run it
    cdo_command = "cdo -aexpr," + expr
    run_this(cdo_command, self, output = "ensemble")



def sum_all(self, drop = True):
    """
    Calculate the sum of all variables for each time step

    Parameters
    -------------
    drop : boolean
        Do you want to keep variables?
    """

    if type(self) is list:
        raise TypeError("This only works for single files presently")

    self.release()

    if drop == True:
        self.transmute({"total":"+".join(self.variables)})

    else:
        if "total" not in self.variables:
            self.mutate({"total":"+".join(self.variables)})
        else:
            i = 0
            while True:
                if "total" + str(i) not in self.variables:
                    break
                i += 1
            self.mutate({"total" + str(i):"+".join(self.variables)})












