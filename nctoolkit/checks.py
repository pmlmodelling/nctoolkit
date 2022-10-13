import xarray as xr
from nctoolkit.temp_file import temp_file
from nctoolkit.api import open_data
from netCDF4 import Dataset
import subprocess
import warnings

def is_corrupt(self):
    """
    Check if files are corrupt 
    """

    for ff in self:

        the_temp = temp_file() + "nc"
        command = f"cdo -copy {ff}  {the_temp}"
        out = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        result, ignore = out.communicate()
        if "error" in str(result):
            print(f"{ff} appears to be corrupt")
            return True
        else:
            blash = None
    return False



def check(self):
    """
    Check contents of files for common data problems.
    """

    print("*****************************************")
    print("Checking data types")
    print("*****************************************")
    try:
        self_contents = self.contents
        list1 = self_contents.reset_index(drop=True).data_type
        positions = [ind for ind, x in enumerate(list1) if x.startswith("I")]
        if len(positions):
            bad = list(self_contents.reset_index(drop=True).data_type[positions])

        if len(positions) > 0:
            check = ",".join(bad)
            if "," in check:
                print(
                    f"The variable(s) {check} have integer data type. Consider setting data type to float 'F64' or 'F32' using set_precision."
                )
            else:
                print(
                    f"The variable {check} has integer data type. Consider setting data type to float 'F64' or 'F32' using set_precision."
                )
        else:
            print("Variable checks passed")
    except:
        print("Unable to check data types. This file is likely not CF-compliant")

    print("*****************************************")
    print("Checking time data type")
    print("*****************************************")

    try:
        the_warns = []
        for ff in self:
            dataset = Dataset(ff)
            times = [x for x in dataset.variables.keys() if "time" in x]
            if len(times) > 0:
                for tt in times:
                    time_var = dataset.variables[tt][:]
                    if "int" in str(time_var.dtype):
                        the_warns.append(f"{tt} has integer data type. Consider setting it to double using as_double")


        if len(the_warns) > 0:
            the_warns = list(set(the_warns))
            for tt in the_warns:
                print(tt)
    except:
        print("Unable to check data types. This file is likely not CF-compliant")

    print("*****************************************")
    print("Running CF-compliance checks")
    print("*****************************************")


    cf_checker = True
    try:
        import cfchecker
    except:
        cf_checker = False
        print(
            "cfchecker is not available. Run 'pip install cfchecker' to check files for CF-compliance!"
        )

    if cf_checker:
        try:
            for ff in self:
                version = ""
                try:
                    ds = xr.open_dataset(ff, decode_times=False)
                    if "Conventions" not in list(ds.attrs.keys()):
                        print(f"No CF-conventions in {ff}")
                    else:
                        version = ds.attrs["Conventions"].split("-")[1]
                except:
                    warnings.warn("Note: there are issues opening this file using xarray. You may want to look closely to see if there are formatting issues that will have negative downstream impacts!")

                if len(version) > 0:
                    command = f"cfchecks -v {version} {ff}"
                else:
                    command = f"cfchecks {ff}"

                out = subprocess.Popen(
                    command,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                result, ignore = out.communicate()

                result_split = result.decode("utf-8").split("\n")
                splits = [
                    index
                    for index, value in enumerate(result_split)
                    if "Checking variable" in value
                ]
                end = [
                    index
                    for index, value in enumerate(result_split)
                    if "ERRORS dete" in value
                ][0]
                for i in range(0, len(splits)):
                    if i < (len(splits) - 1):

                        i_result = result_split[splits[i] : splits[i + 1]]
                        i_result = "\n".join(i_result)
                        if "ERROR: " in i_result:
                            i_result = i_result.replace(
                                "Checking variable:", "Issue with variable:"
                            )
                            print(i_result)
                    else:
                        i_result = result_split[splits[i] : end]
                        i_result = "\n".join(i_result)
                        if "ERROR: " in i_result:
                            i_result = i_result.replace(
                                "Checking variable:", "Issue with variable:"
                            )
                            print(i_result)
        except:
            warnings.warn("Problem running CF-compliance checks. Have a look at the cfchecker installation")

    print("*****************************************")
    print("Checking grid consistency")
    print("*****************************************")

    try:
        for ff in self:
            command = f"cdo griddes {ff}"
            out = subprocess.Popen(
                command,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            result, ignore = out.communicate()

            result = result.decode("utf-8")
            if result.count("gridID") > 1:
                print("Dataset file(s) contain variables with different grids.")
    except:
        print("Unable to check grid. This dataset might not be CF-compliant!")
