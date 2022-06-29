import re
import dill
import inspect
import numpy as np
import nctoolkit as nc

session_info = nc.session.session_info

def is_lambda(v):
    LAMBDA = lambda: 0
    return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__


class DataSet(object):
    
    def _init_(self):
        self.data = None
    
    def assign(self, drop=False, **kwargs):
        """
        Create new variables
        Existing columns that are re-assigned will be overwritten.
    
        Parameters
        ----------
        drop : bool
            Set to True if you want existing variables to be removed once the new ones have been created.
            Defaults to False.
    
            should evaluate to a numeric. New variables are calculated for each grid cell and time step.
        **kwargs : dict of {str: callable}
            New variable names are keywords. All terms in the equation given by the lamda function
            should evaluate to a numeric. New variables are calculated for each grid cell and time step.
        Notes
        -----
        Operations are carried out in the order give. So if a new variable is created in the first argument,
        it can then be used in following arguments.
    
    
    
    
        """
        frame = inspect.currentframe()
    
        if type(drop) is not bool:
            raise ValueError("drop is not boolean!")
    
        if len(kwargs) == 0:
            raise ValueError("Please provide assignments!")
    
        for k, v in kwargs.items():
            if is_lambda(v) is False:
                raise ValueError("Please check everything is a lambda function!")
            lambdas = v
    
        for k, v in kwargs.items():
            if is_lambda(v) is True:
                break
        lambdas = v
    
        # now, we need to parse things.
    
        interactive = False
        if session_info["interactive"]:
            import readline
    
            if readline.get_current_history_length() > 0:
                interactive = True
        try:
            start = lambdas
            try:
                all_str = list(inspect.getsourcelines(start))[0]
                all_str = "".join(all_str)
                start = all_str.replace("'", "").replace("\\n", "")[1:-1].replace("  ", " ")
                start = start.replace("\n", "")
            except:
                start = dill.source.getsource(start).replace("\n", "").strip()
        except:
    
            if interactive:
                import readline
    
                start = [
                    str(readline.get_history_item(i + 1))
                    for i in range(readline.get_current_history_length())
                ]
                i = 0
                for ss in start:
                    if ".assign(" in ss:
                        ind = i
                    i += 1
    
                all_str = start[ind : len(start)]
                all_str = "".join(all_str)
                start = all_str.replace("'", "").replace("\\n", "").replace("  ", " ")
            else:
                start = lambdas
                try:
                    all_str = list(inspect.getsourcelines(start))[0]
                    all_str = "".join(all_str)
                    start = (
                        all_str.replace("'", "").replace("\\n", "")[1:-1].replace("  ", " ")
                    )
    
                except:
                    start = dill.source.getsource(start).replace("\n", "").strip()
    
        # we now need to figure out if what we have is one line
    
        if ";" in start:
            raise ValueError("You cannot split assign calls using ;")
        if ".assign(" not in start:
            if interactive:
                raise ValueError(f"Found {start} as the first lin history")
            raise ValueError("Please write assign methods as single line!")
            
ds = DataSet()
ds.assign(y = lambda  x: x.y + 273)
