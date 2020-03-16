import copy

from .temp_file import temp_file
from .session import nc_safe
from .flatten import str_flatten
from .select import select_variables
from .setters import set_longnames
from .cleanup import cleanup
from .cleanup import disk_clean
from .runthis import run_cdo
from .show import nc_years
import copy


def phenology(self, var = None, metric = None, p = None):
    """
    Calculate phenologies from a dataset. Each file in an ensemble must only cover a single year, and ideally have all days.
    This method currently only calculcates the day of year of the annual maximum.

    Parameters
    -------------
    var : str
        Variable to analyze.
    metric : str
        Must be peak, middle, start or end
    p : str
        Percentile to use for start or end
    """

    if metric is None:
        raise ValueError("No metric was supplied!")

    if var is None:
        raise ValueError("No var was supplied")
    if type(var) is not str:
        raise TypeError("var is not a str")

    self.release()


    if metric == "peak":

        new_files = []
        new_commands = []

        for ff in self:
            if len(nc_years(ff)) > 1:
                raise ValueError("This can only work with single year data currently")

            target = temp_file(".nc")
            command = f"cdo -L -timmin -setrtomiss,-10000,0 -expr,'peak=var*ctimestep()' -eq -chname,{var},var -selname,{var} {ff} -timmax -chname,{var},var -selname,{var} {ff} {target}"

            target = run_cdo(command, target = target)

            new_files.append(target)
            new_commands.append(command)

        self.history.append(new_commands)
        self._hold_history = copy.deepcopy(self.history)

        self.current = new_files

        if len(self.current) == 1:
            self.current = self.current[0]

        cleanup()
        return None




    if metric == "start" or metric == "end" or metric == "middle":

        if metric == "middle":
            p = 50.0

        if type(p) is int:
            p = float(p)

        if type(p) is not float:
            raise TypeError("p is not float")

        start = (100 - p)/100
        new_files = []
        new_commands = []

        for ff in self:

            if len(nc_years(ff)) > 1:
                raise ValueError("This can only work with single year data currently")

            target = temp_file(".nc")
            command = f"cdo -L -timmin -setrtomiss,-10000,0 -expr,'{metric}=var*ctimestep()' -gt -timcumsum -chname,{var},var -selname,{var} {ff} -mulc,{start} -timsum -chname,{var},var -selname,{var} {ff} {target}"

            target = run_cdo(command, target = target)

            new_files.append(target)
            new_commands.append(command)

        self.history.append(new_commands)
        self._hold_history = copy.deepcopy(self.history)

        self.current = new_files

        if len(self.current) == 1:
            self.current = self.current[0]
        cleanup()

        return None


        raise ValueError("You have not supplied a valid metric")


