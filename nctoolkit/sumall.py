import inspect
import warnings

from nctoolkit.runthis import run_this




def sum_all(self, drop=True):
    """
    Calculate the sum of all variables for each time step

    Parameters
    -------------
    drop : boolean
        Do you want to keep variables?
    """

    self.run()

    if (len(self) > 1) and (self._merged is False):
        raise TypeError("This only works for single files presently")

    if drop is True:
        # self.transmute({"total": "+".join(self.variables)})
        self.cdo_command("expr,total=" + "+".join(self.variables))

    else:
        if "total" not in self.variables:
            self.cdo_command("aexpr,total=" + "+".join(self.variables))
        else:
            i = 0
            while True:
                if f"total{i}" not in self.variables:
                    break
                i += 1
            self.cdo_command("aexpr,total" + str(i) + "=" + "+".join(self.variables))
