
from ._cleanup import cleanup
from ._runthis import run_this
import sys


def fix_expr(expr):
    """Function to fix expressions that use locals"""

    expr = ''.join((' {} '.format(el) if el in '=><+-/*^()' else el for el in expr))
    expr_split = expr.split(" ")
    new_expr = ""

    for x in expr_split:
        if x.startswith("@"):
            # We need to first check the local variable supplied is a numeric
            if (isinstance(eval("sys.modules['__main__']." + x.replace("@", "")), (int, float))) == False:
                raise ValueError(x +  " is not numeric!")
            new_expr +=  str(eval("sys.modules['__main__']." + x.replace("@", "")))
        else:
            new_expr +=  x
    return new_expr

def expression(self, operations = None, method = "expr", silent = True, cores = 1):
    """Method to modify a netcdf file using expr"""

    if type(operations) is not dict:
        raise ValueError("No expression was provided")

    # first,we need to convert the operations dictionary to a cdo expression 

    expr = []

    for key,value in operations.items():
        expr.append(key + "=" + fix_expr(value))
        
    expr = ";".join(expr)
    expr = expr.replace(" ", "" )
    expr = '"' + expr + '"'


    cdo_command = "cdo -" + method + "," + expr
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)    


def transmute(self, operations = None, silent = True, cores = 1):
    return expression(self, operations = operations, method = "expr", silent = silent, cores = cores)


def mutate(self, operations = None, silent = True, cores = 1):
    return expression(self, operations = operations, method = "aexpr", silent = silent, cores = cores)



