import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_cdo, tidy_command
from nctoolkit.show import nc_years
from nctoolkit.temp_file import temp_file
from nctoolkit.session import remove_safe
from nctoolkit.show import nc_variables


def phenology(self, var=None, metric=None, p=None):
    """
    Calculate phenologies from a dataset
    Each file in an ensemble must only cover a single year, and ideally have all days.
    The method assumes datasets have daily resolution.

    Parameters
    -------------
    var : str
        Variable to analyze.
    metric : str
        Must be peak, middle, start or end. Peak is defined as the day of the maximum
        value.  Middle is the day when the cumulative total of the variable first
        exceeds the cumulative total for the entire year. Start or end is defined as
        the first day when the cumulative total exceeds a percentile p of the maximum
        cumulative total.
    p : str
        Percentile to use for start or end.
    """

    if len(self) == 0:
        raise ValueError("Failure due to empty dataset!")

    if metric is None:
        raise ValueError("No metric was supplied!")

    if metric not in ["peak", "middle", "start", "end"]:
        raise ValueError(f"{metric} is not a valid metric")

    if var is None:
        raise ValueError("No var was supplied")
    if not isinstance(var, str):
        raise TypeError("var is not a str")

    self.run()

    # split data into separate years if needed
    split_files = False
    for ff in self:
        if len(nc_years(ff)) > 1:
            split_files = True

    for ff in self:
        if var not in nc_variables(ff):
            raise ValueError(f"{var} is not a valid variable!")

    if split_files:
        self.split("year")

    if metric == "peak":

        new_files = []
        new_commands = []

        for ff in self:

            target = temp_file(".nc")
            command = (
                f"cdo -timmin -setrtomiss,-10000,0 -expr,'peak=var*ctimestep()' "
                f"-eq -chname,{var},var -selname,{var} {ff} -timmax -chname,{var},var "
                f"-selname,{var} {ff} {target}"
            )

            command = tidy_command(command)
            target = run_cdo(command, target=target, precision=self._precision)

            new_files.append(target)
            new_commands.append(command)

        self.history.append(new_commands)
        self._hold_history = copy.deepcopy(self.history)

        self.current = new_files

        for ff in new_files:
            remove_safe(ff)

        cleanup()
        return None

    if (metric == "start") or (metric == "end") or (metric == "middle"):

        if metric == "middle":
            p = 50.0

        if (metric == "start") and (p is None):
            p = 25.0

        if (metric == "end") and (p is None):
            p = 75.0

        if isinstance(p, int):
            p = float(p)

        if not isinstance(p, float):
            raise TypeError("p is not float")

        start = (p) / 100
        new_files = []
        new_commands = []

        for ff in self:

            target = temp_file(".nc")
            command = (
                f"cdo -timmin -setrtomiss,-10000,0 -expr,"
                f"'{metric}=var*ctimestep()' -gt -timcumsum -chname,{var},var "
                f"-selname,{var} {ff} -mulc,{start} -timsum -chname,{var},var "
                f"-selname,{var} {ff} {target}"
            )

            command = tidy_command(command)
            target = run_cdo(command, target=target, precision=self._precision)

            new_files.append(target)
            new_commands.append(command)

        self.history.append(new_commands)
        self._hold_history = copy.deepcopy(self.history)

        self.current = new_files

        for ff in new_files:
            remove_safe(ff)

        cleanup()

        return None
