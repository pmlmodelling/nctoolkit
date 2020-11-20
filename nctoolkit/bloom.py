import copy

from nctoolkit.cleanup import cleanup
from nctoolkit.runthis import run_cdo, tidy_command
from nctoolkit.show import nc_years
from nctoolkit.temp_file import temp_file
from nctoolkit.api import open_data
from nctoolkit.session import nc_safe
from nctoolkit.show import nc_variables


def initiation(self, var=None, metric="Henson", threshold = 0.05):

    if type(threshold) is not float:
        raise ValueError("threshold must be a float")

    if threshold <=0 or threshold >= 1:
        raise ValueError(f"{threshold} is not a meaningful threshold")

    if var is None:
        raise TypeError("Please supply a variable")

    for ff in self:
        if var not in nc_variables(ff):
            raise ValueError(f"{var} is not a valid variable!")

    if metric == "Henson":

        new_files = []
        new_commands = []

        for ff in self:

            target = temp_file(".nc")
            command = f"cdo -ltc,1 -timcumsum -setrtomiss,-10000,0 -expr,'peak=var*ctimestep()' "\
                f"-eq -chname,{var},var -selname,{var} {ff} -timmax -chname,{var},var "\
                f"-selname,{var} {ff} {target}"

            command = tidy_command(command)
            target = run_cdo(command, target=target)
            nc_safe.append(target)

            # calculate the maximum
            data_max = open_data(ff)
            n_times = len(data_max.times)
            data_max.select_variables(var)
            data_max.max()
            data_max.rename({var:"max"})
            data_max.run()

            # calculate the maximum
            data_median = open_data(ff)
            n_times = len(data_median.times)
            data_median.select_variables(var)
            data_median.median()
            data_median.rename({var:"median"})
            data_median.run()

            # calculate the pre-bloom minimum
            data_min = open_data(ff)
            data_min.multiply(target)

            data_henson = data_min.copy()

            data_min.set_missing(0)
            data_min.min()
            data_min.rename({var:"min"})
            data_min.run()

            # now calculate whether the variabe exceeds the peak

            data_henson.rename({var:"var"})
            data_henson.append(data_min)
            data_henson.append(data_max)
            data_henson.append(data_median)

            data_henson.merge(match = "year")
            data_max5 = data_henson.copy()
            data_median5 = data_henson.copy()
            data_henson.transmute({"result":f"(var-min)/(max-min) > {threshold}"})
            data_henson.transmute({"start_henson":"result * ctimestep()"})
            data_henson.set_missing(0)
            data_henson.min()
            data_henson.run()

            data_max5.transmute({"result":f"(var)/(max) > {threshold}"})
            data_max5.transmute({"start_max":"result * ctimestep()"})
            data_max5.set_missing(0)
            data_max5.min()
            data_max5.run()


            data_median5.transmute({"result":f"(var)/(median) > {threshold}"})
            data_median5.transmute({"start_median":"result * ctimestep()"})
            data_median5.set_missing(0)
            data_median5.min()
            data_median5.run()

            data_max5.append(data_henson)
            data_max5.append(data_median5)
            data_max5.merge()
            data_max5.set_longnames({"start_max":"First day when chl exceeds 5% of max"})
            data_max5.set_longnames({"start_median":"First day when chl exceeds 5% of median"})
            data_max5.set_longnames({"start_henson":"First day when chl exceeds 5% of the diff between min/max"})

            data_max5.set_units({"start_max":"Day of year"})
            data_max5.set_units({"start_median":"Day of year"})
            data_max5.set_units({"start_henson":"Day of year"})
            data_max5.run()

            new_files.append(data_max5.current)

            nc_safe.remove(target)


        self.history.append(new_commands)
        self._hold_history = copy.deepcopy(self.history)

        self.current = new_files

        cleanup()
        return None


