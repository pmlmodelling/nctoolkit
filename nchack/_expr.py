
from ._cleanup import cleanup
from ._runthis import run_this

def expression(self, operations = None, method = "expr", silent = True, cores = 1):
    """Method to modify a netcdf file using expr"""

    if type(operations) is not dict:
        raise ValueError("No expression was provided")

    # first,we need to convert the operations dictionary to a cdo expression 

    expr = []

    for key,value in operations.items():
        expr.append(key + "=" + value)
        
    expr = ";".join(expr)
    expr = expr.replace(" ", "" )
    expr = '"' + expr + '"'

    cdo_command = "cdo " + method + "," + expr
    run_this(cdo_command, self, silent, output = "ensemble", cores = cores)
    
    cleanup(keep = self.current)    


def transmute(self, operations = None, silent = True, cores = 1):
    return expression(self, operations = operations, method = "expr", silent = silent, cores = cores)


def mutate(self, operations = None, silent = True, cores = 1):
    return expression(self, operations = operations, method = "aexpr", silent = silent, cores = cores)



