
import copy

from nctoolkit.cleanup import cleanup, disk_clean
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_cdo, tidy_command
from nctoolkit.select import select_variables
from nctoolkit.session import nc_safe
from nctoolkit.setters import set_longnames
from nctoolkit.show import nc_years
from nctoolkit.temp_file import temp_file


def phenology(self, var=None, metric=None, p=None):
    """
    Calculate phenologies from a dataset
    Each file in an ensemble must only cover a single year, and ideally have all days. The method assumes datasets have daily resolution.

    Parameters
    -------------
    var : str
        Variable to analyze.
    metric : str
        Must be peak, middle, start or end. Peak is defined as the day of the maximum value. Middle is the day when the cumulative total of the variable first exceeds the cumulative total for the entire year. Start or end is defined as the first day when the cumulative total exceeds a percentile p of the maximum cumulative total.
    p : str
        Percentile to use for start or end.
    """

    if metric is None:
        raise ValueError("No metric was supplied!")

    if var is None:
        raise ValueError("No var was supplied")
    if type(var) is not str:
        raise TypeError("var is not a str")

    self.run()

    if metric == "peak":

        new_files = []
        new_commands = []

        for ff in self:
            if len(nc_years(ff)) > 1:
                raise ValueError("This can only work with single year data currently")

            target = temp_file(".nc")
            command = f"cdo -timmin -setrtomiss,-10000,0 -expr,'peak=var*ctimestep()' -eq -chname,{var},var -selname,{var} {ff} -timmax -chname,{var},var -selname,{var} {ff} {target}"

            command = tidy_command(command)
            target = run_cdo(command, target=target)

            new_files.append(target)
            new_commands.append(command)

        self.history.append(new_commands)
        self._hold_history = copy.deepcopy(self.history)

        self.current = new_files

        cleanup()
        return None

    if (metric == "start") or (metric == "end") or (metric == "middle"):

        if metric == "middle":
            p = 50.0

        if (metric == "start") and (p is None):
            p = 25.0

        if (metric == "end") and (p is None):
            p = 75.0

        if type(p) is int:
            p = float(p)

        if type(p) is not float:
            raise TypeError("p is not float")

        start = (p) / 100
        new_files = []
        new_commands = []

        for ff in self:

            if len(nc_years(ff)) > 1:
                raise ValueError("This can only work with single year data currently")

            target = temp_file(".nc")
            command = f"cdo -timmin -setrtomiss,-10000,0 -expr,'{metric}=var*ctimestep()' -gt -timcumsum -chname,{var},var -selname,{var} {ff} -mulc,{start} -timsum -chname,{var},var -selname,{var} {ff} {target}"

            command = tidy_command(command)
            target = run_cdo(command, target=target)

            new_files.append(target)
            new_commands.append(command)

        self.history.append(new_commands)
        self._hold_history = copy.deepcopy(self.history)

        self.current = new_files

        cleanup()

        return None

    raise ValueError("You have not supplied a valid metric")
