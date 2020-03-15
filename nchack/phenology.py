import copy

from .temp_file import temp_file
from .session import nc_safe
from .flatten import str_flatten
from .select import select_variables
from .setters import set_longnames
from .cleanup import cleanup
from .cleanup import disk_clean
from .runthis import run_cdo
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

    # First step is to check if the current file exists
    if type(self.current) is not str:
        raise TypeError("This method only works on single files")

    if len(self.years()) > 1:
        raise ValueError("This can only work with single year data currently")

    if metric == "middle":

        new_files = []
        new_commands = []

        for ff in self:

            target = temp_file(".nc")
            command = f"cdo -L -timmin -setrtomiss,-10000,0 -expr,'middle=var*ctimestep()' -gt -timcumsum -chname,{var},var -selname,{var} {ff} -divc,2 -timsum -chname,{var},var -selname,{var} {self.current} {target}"

            target = run_cdo(command, target = target)

            new_files.append(ff)
            new_commands.append(ff)


        self.history.append(new_commands)
        self._hold_history = copy.deepcopy(self.history)

        self.current = new_files

        if len(self.current) == 1:
            self.current = self.current[0]

        return None

    if metric == "peak":
        target = temp_file(".nc")
        command = f"cdo -L -timmin -setrtomiss,-10000,0 -expr,'peak=var*ctimestep()' -eq -chname,{var},var -selname,{var} {self.current} -timmax -chname,{var},var -selname,{var} {self.current} {target}"

        target = run_cdo(command, target = target)
        self.history.append(command)
        self._hold_history = copy.deepcopy(self.history)

        self.current = target

        return None

    if metric == "start" or metric == "end":
        if type(p) is not float:
            raise TypeError("p is not float")

        start = (100 - p)/100

        target = temp_file(".nc")
        command = f"cdo -L -timmin -setrtomiss,-10000,0 -expr,'middle=var*ctimestep()' -gt -timcumsum -chname,{var},var -selname,{var} {self.current} -multc,{start} -timsum -chname,{var},var -selname,{var} {self.current} {target}"

        target = run_cdo(command, target = target)
        self.history.append(command)
        self._hold_history = copy.deepcopy(self.history)
        self.current = target

        return None

    cleanup(self.current)

    self.disk_clean()



