import copy
import os
import re
import subprocess
import platform
import warnings
import multiprocessing
import signal

from nctoolkit.cleanup import cleanup
from nctoolkit.flatten import str_flatten
from nctoolkit.session import (
    session_info,
    append_safe,
    remove_safe,
    get_protected,
)
from nctoolkit.temp_file import temp_file

from nctoolkit.show import nc_variables

from nctoolkit.utils import version_below


def file_size(file_path):
    """
    A function to return file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size


def tidy_command(command):

    if session_info["precision"] is not None:
        command = command.replace("cdo ", "cdo -b " + session_info["precision"] + " ")

    command = command.replace("  ", " ")

    if " --sortname " in command:
        command = command.replace(" --sortname ", " ")
        command = command.replace("cdo ", "cdo --sortname ")

    if "reduce_dim" in command:
        command = (
            command.replace("reduce_dim", "").replace(" - ", " ").replace(" -- ", " ")
        )
        command = command.replace("cdo ", "cdo --reduce_dim ")

    command = command.strip()

    if session_info["thread_safe"] is False:
        command = command.replace("-L ", " ").replace("cdo ", "cdo -L ")
    else:
        command = command.replace("-L ", " ")

    return command


def run_nco(command, target, out_file=None, overwrite=False):
    command = command.strip()
    append_safe(target)
    if (
        command.startswith("ncea ")
        or command.startswith("ncra ")
        or command.startswith("ncap ")
        or command.startswith("ncap2 ")
        or command.startswith("ncks ")
        or command.startswith("ncrename ")
        or command.startswith("ncatted")
    ) is False:
        raise ValueError("This is not a valid NCO command")

    # Make sure it is not attempting to overwrite a protected file
    if out_file is None:
        if command.split()[-1] in get_protected():
            if overwrite is False:
                raise ValueError("Attempting to overwrite an opened file")

    if platform.system() == "Linux":
        if session_info["temp_dir"] == "/tmp/":
            result = os.statvfs("/tmp/")
            result = result.f_frsize * result.f_bavail

            if result < 1 * 1e9:
                session_info["temp_dir"] == "/var/tmp/"
                if target.startswith("/tmp"):
                    new_target = target.replace("/tmp/", "/var/tmp/")
                    command = command.replace(target, new_target)
                    remove_safe(target)
                    target = new_target
                    append_safe(target)

    out = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    result, ignore = out.communicate()

    if "(Abort)" in str(result):
        raise ValueError(
            str(result).replace("b'", "").replace("\\n", "").replace("'", "")
        )

    if "ERROR" in str(result):
        if target.startswith("/tmp/"):
            new_target = target.replace("/tmp/", "/var/tmp/")
            command = command.replace(target, new_target)
            append_safe(new_target)
            remove_safe(target)
            target = new_target

            out = subprocess.Popen(
                command,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            result1, ignore = out.communicate()
            if "ERROR" in str(result1):
                remove_safe(target)
                raise ValueError(
                    str(result1).replace("b'", "").replace("\\n", "").replace("'", "")
                )
            session_info["temp_dir"] = "/var/tmp/"
            if "Warning:" in str(result1):
                warnings.warn(message=f"NCO warning: {str(result1)}")
    else:
        if "Warning:" in str(result):
            warnings.warn(message=f"NCO warning: {str(result)}")

    if target != "":
        if os.path.exists(target) is False:
            remove_safe(target)
            raise ValueError(f"{command} was not successful. Check output")
    else:
        actual_target = command.split(" ")[-1].strip()
        if os.path.exists(actual_target) is False:
            remove_safe(target)
            raise ValueError(f"{command} was not successful. Check output")

    if target != "":
        session_info["latest_size"] = os.path.getsize(target)

    return target


def run_cdo(command=None, target=None, out_file=None, overwrite=False, precision=None):

    warned = False

    if not isinstance(precision, str):
        raise ValueError("Precision must be str")

    if precision not in ["I8", "I16", "I32", "F32", "F64", "default"]:
        raise ValueError(f"Precision - {precision} - is not valid")

    if precision in ["I8", "I16", "I32", "F32", "F64"]:
        if " -b " not in command:
            command = command.replace("cdo ", f"cdo -b {precision} ")

    # make sure the output file does not exist

    command = tidy_command(command)
    start_target = target

    if out_file is None:
        if os.path.exists(command.split()[-1]):
            if overwrite is False:
                raise ValueError("Attempting to overwrite file")

    if platform.system() == "Linux":
        if session_info["temp_dir"] == "/tmp/":
            result = os.statvfs("/tmp/")
            result = result.f_frsize * result.f_bavail

            if result < 1 * 1e9:
                session_info["temp_dir"] == "/var/tmp/"
                if target.startswith("/tmp"):
                    new_target = target.replace("/tmp/", "/var/tmp/")
                    command = command.replace(target, new_target)
                    target = target.replace("/tmp/", "/var/tmp/")
    append_safe(target)

    if command.startswith("cdo ") is False:
        raise ValueError("The command does not start with cdo!")

    out = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    out.wait()
    result, ignore = out.communicate()

    # If it is a generic grid, it's better to not throw the CDO error which might be confusing.
    if "generic" in result.decode("utf-8").lower():
        if "unsupported" in result.decode("utf-8").lower():
            raise ValueError(
                "Dataset contains generic grids. Please fix to lonlat or curvilinear"
            )

    # this will potentially fail because of floating point precision. A quick fix to see if that is the case....
    if "Use the CDO option -b F32" in (
        result.decode("utf-8")
    ) or "not represent" in result.decode("utf-8"):
        print("Switching to 32 bit precision!")
        command_chunks = command.split(" ")

        i = 0
        change = None
        for cc in command_chunks:
            i += 1
            if "-b" == cc.strip():
                change = i
        if change is not None:
            command_chunks[change] = "32"
            command = str_flatten(command_chunks, " ")
        else:
            command = command.replace("cdo ", "cdo -b 32 ")

        if os.path.exists(target):
            if out_file is None:
                os.remove(target)
                remove_safe(target)

        new_target = temp_file("nc")
        append_safe(new_target)
        command = command.replace(target, new_target)
        target = new_target

        out = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        out.wait()
        result, ignore = out.communicate()

    if "Use the CDO option -b F32" in (result.decode("utf-8")):
        command_chunks = command.split(" ")

        i = 0
        change = None
        for cc in command_chunks:
            i += 1
            if "-b" == cc.strip():
                change = i
        if change is not None:
            command_chunks[change] = "F32"
            command = str_flatten(command_chunks, " ")
        else:
            command = command.replace("cdo ", "cdo -b F64 ")
        command

        out = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        out.wait()
        result, ignore = out.communicate()

    if out_file is not None:
        if "HDF5 library version mismatched error" in str(result):
            remove_safe(target)
            remove_safe(start_target)
            raise ValueError(
                "The HDF5 header files used to compile this application do not match "
                "the version used by the HDF5 library to which this application is "
                "linked. This is likely because of a conda problem."
            )

        if (
            str(result).startswith("b'Error")
            or ("HDF error" in str(result))
            or (out.returncode != 0)
        ):
            remove_safe(target)
            remove_safe(start_target)
            raise ValueError(
                "HDF error when running CDO. Check if files are corrupt using the is_corrupt method, and consider running the check method"
            )
        else:
            return out_file

    if ("sellonlat" in command) and ("std::bad_alloc" in str(result)):
        remove_safe(target)
        remove_safe(start_target)
        raise ValueError(
            "Is the horizontal grid very large? Consider setting cdo=False in crop!"
        )

    if "cdf_put" in str(result):
        error = str(result).replace("b'", "").replace("\\n", "").replace("'", "")
        if "Numeric conversion not representable" in error:
            error = f"Processing error in CDO. Please check your dataset data types and run check on the dataset: {error}."
            raise ValueError(error)

    if "(Abort)" in str(result):
        remove_safe(target)
        remove_safe(start_target)
        error = str(result).replace("b'", "").replace("\\n", "").replace("'", "")

        text = re.compile(r"Level [0-9]* not found")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            error = [str(int(x) + 1) for x in re.findall(r"\d+", error)]
            raise ValueError(f"None of the vertical levels supplied are available!")

        text = re.compile(r"Date between .* not found")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            raise ValueError(
                f"Please check dates supplied to nctoolkit".replace("  ", " ")
            )

        if "gridcell_areas" in error:
            if "Cell corner coordinates missing!" in error:
                raise ValueError(
                    "CDO was uanable to calculate cell areas because cell corner coordinates are missing"
                )

        if "genbil" in error:
            if "support unstructured source grids" in error:
                raise ValueError(
                    "Unable to regrid an unstructured grid. Considering using nearest neighbour!"
                )

        if "Unsupported grid" in error:
            if "unstructured" in error.lower():
                raise ValueError("This method does not supported unstructured grids!")

        if "Too many different grids" in error:
            raise ValueError(
                "Error in internal CDO processing. Too many different grids for method. Consider subsetting to specific variables!"
            )

        text = re.compile(r"Variable >.*< not found!")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            raise ValueError(
                f"None of the variables were found. Please check variables supplied to nctoolkit"
            )

        text = re.compile(r" Variable name .* not found!")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0].strip()
            raise ValueError(f"{error}! Please check variables supplied to nctoolkit")

        text = re.compile(r"File has less then [0-9]* timesteps!")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            raise ValueError(
                f"{error}! Please check time steps supplied to nctoolkit methods"
            )

        text = re.compile(r"Grid size of the input parameter .* do not match!")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            raise ValueError(
                f"Grid sizes are not consistent. Please check grids in datasets used in operation!"
            )

        text = re.compile(r"Season .* not found")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            error = error.split(">")[1].split("<")[0]
            raise ValueError(
                f"The following seasons were not available: {error}. Please check season supplied to nctoolkit methods!"
            )

        text = re.compile(r"Month [0-9]* not found")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            raise ValueError(
                f"None of the months supplied are in the dataset. Please check months supplied to nctoolkit methods!"
            )

        text = re.compile(r"month [0-9]* not found")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            raise ValueError(
                f"None of the months supplied are in the dataset. Please check months supplied to nctoolkit methods!"
            )

        text = re.compile(r"Year [0-9]* not found")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            raise ValueError(
                f"None of the years are available. Please check years supplied to nctoolkit methods!"
            )

        text = re.compile(r"Day [0-9]* not found")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            raise ValueError(
                f"None of the days supplied are available. Please check days supplied to nctoolkit methods!"
            )


        text = re.compile(r"Timestep [0-9]* not found")
        errors = text.findall(error)
        if len(errors) > 0:
            error = errors[0]
            error = [str(int(x) - 1) for x in re.findall(r"\d+", error)]
            error = ",".join(error)
            error = "The following timesteps do not exist: " + error
            raise ValueError(
                f"{error}! Please check time steps supplied to nctoolkit methods"
            )

        raise ValueError(
            str(result).replace("b'", "").replace("\\n", "").replace("'", "")
        )

    if "HDF5 library version mismatched error" in str(result):
        raise ValueError(
            "The HDF5 header files used to compile this application do not match "
            "the version used by the HDF5 library to which this application is "
            "linked. This is likely because of a conda problem."
        )

    if (
        (str(result).startswith("b'Error"))
        or ("HDF error" in str(result))
        or (out.returncode != 0)
    ):
        if target.startswith("/tmp/"):
            new_target = target.replace("/tmp/", "/var/tmp/")
            command = command.replace(target, new_target)
            target = new_target
            append_safe(target)

            if "HDF error" in str(result):
                raise ValueError(
                    "HDF error when running CDO. Check if files are corrupt using the is_corrupt method, and consider running the check method"
                )

            out = subprocess.Popen(
                command,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            out.wait()
            result1, ignore = out.communicate()
            if (
                (str(result1).startswith("b'Error"))
                or ("HDF error" in str(result1))
                or (out.returncode != 0)
            ):
                if "Too many open files" in str(result1):
                    remove_safe(target)
                    remove_safe(start_target)
                    raise ValueError(
                        "There are too many open files in CDO. Check the files "
                        "your OS allows to be open simultaneously in the Bourne "
                        "shell with 'ulimit -n'"
                    )
                else:
                    remove_safe(target)
                    remove_safe(start_target)

                    if (
                        "Error (cdf_put_vara_double): NetCDF: Numeric conversion not representable"
                        in str(result)
                    ):
                        raise ValueError(
                            "CDO error: Error (cdf_put_vara_double): NetCDF: Numeric conversion not representable. Tip: Consider changing numerical precision using set_precision or check if missing values are incorrectly set to large actual values!"
                        )

                    raise ValueError(
                        str(result1)
                        .replace("b'", "")
                        .replace("\\n", "")
                        .replace("'", "")
                    )
            session_info["temp_dir"] = "/var/tmp/"

            # loop through the warnings

            messages = str(result1).split("\\n")

            missing_years = []
            missing_months = []
            for x in messages:
                if "Warning:" in x:
                    print_result1 = True
                    if ("merge" in x) and ("Duplicate entry of parameter" in str(x)):
                        print_result1 = False

                    # deal with warning messages for selecting months
                    pattern = re.compile(r"Year \d{4} not found")
                    if pattern.search(x):
                        print_result1 = False
                        d = re.findall("\d{4}", x)
                        missing_years.append(d[0])

                    pattern = re.compile(r"Month ([1-9][0-9]?|100) not found")
                    if pattern.search(x):
                        print_result1 = False
                        d = re.findall("([1-9][0-9]?|100)", x)
                        missing_months.append(d[0])
                    if print_result1:
                        warnings.warn(
                            message="CDO warning:"
                            + x.replace("b'Warning:", "").replace("Warning:", "")
                        )
                        warned = True

            if len(missing_years) > 0:
                warnings.warn(
                    message=f'CDO warning: Years {str_flatten(missing_years, ",")} '
                    "are missing",
                    stacklevel=2,
                )
                warned = True

            if len(missing_months) > 0:
                warnings.warn(
                    message=f'CDO warning: Months {str_flatten(missing_months, ",")} '
                    "are missing",
                    stacklevel=2,
                )
                warned = True

    else:
        messages = str(result).split("\\n")

        missing_years = []
        missing_months = []
        for x in messages:
            if "Warning:" in x:
                print_result = True
                if ("merge" in x) and ("Duplicate entry of parameter" in str(x)):
                    print_result = False

                # deal with warning messages for selecting months
                pattern = re.compile(r"Year \d{4} not found")

                if pattern.search(x):
                    d = re.findall("\d{4}", x)
                    missing_years.append(d[0])
                    print_result = False

                pattern = re.compile(r"Month ([1-9][0-9]?|100) not found")

                if pattern.search(x):
                    d = re.findall("([1-9][0-9]?|100)", x)
                    missing_months.append(d[0])
                    print_result = False

                if print_result:
                    warnings.warn(
                        message="CDO warning:"
                        + x.replace("b'Warning:", "").replace("Warning:", "")
                    )
                    warned = True

        if len(missing_years) > 0:
            warnings.warn(
                message=f'CDO warning: Years {str_flatten(missing_years, ",")} '
                "are missing!",
                category=Warning,
            )
            warned = True
        if len(missing_months) > 0:
            warnings.warn(
                message=f'CDO warning: Months {str_flatten(missing_months, ",")} '
                "are missing",
                category=Warning,
            )
            warned = True

    if os.path.exists(target) is False:
        remove_safe(target)
        remove_safe(target)
        raise ValueError(f"{command} was not successful. Check output")

    session_info["latest_size"] = os.path.getsize(target)

    sel_year = []
    sel_day = []
    sel_month = []
    sel_level = []
    sel_timestep = []
    sel_hour = []
    sel_var = []


    drop_warnings = []

    for x in result.decode("utf-8").lower().split("\n"):
        warned = False
        ignore = False

        text = re.compile("delete \(warning\): month >[0-9]*< not found!")
        errors = text.findall(x)
        if len(errors) > 0:
            for y in errors:
                for z in re.findall(r'\d+', y):
                    drop_warnings.append(z)
                    #message= f"Warning: Unable to find month {z}"
                    #warnings.warn(message)
                    ignore = True


        if "selyear" in x:
            text = re.compile("selyear \\(warning\\): year [0-9]* not found")
            all_text = text.findall(x)
            if len(all_text) > 0:
                for tt in all_text:
                    sel_year.append(int(re.findall(r"\d+", all_text[0])[0]))
                ignore = True

        if "selhour" in x:
            text = re.compile("selhour \\(warning\\): hour [0-9]* not found")
            all_text = text.findall(x)
            if len(all_text) > 0:
                for tt in all_text:
                    sel_hour.append(int(re.findall(r"\d+", all_text[0])[0]))
                ignore = True

        if "selday" in x:
            text = re.compile("selday \\(warning\\): day [0-9]* not found")
            all_text = text.findall(x)
            if len(all_text) > 0:
                for tt in all_text:
                    sel_day.append(int(re.findall(r"\d+", all_text[0])[0]))
                ignore = True

        if "seltimestep" in x:
            text = re.compile(
                "seltimestep \\(warning\\): timesteps [0-9]*-[0-9]* not found"
            )
            all_text = text.findall(x.replace("  ", " "))
            if len(all_text) > 0:
                for tt in all_text:
                    tt_range = range(
                        int(re.findall(r"\d+", all_text[0])[0]) - 1,
                        int(re.findall(r"\d+", all_text[0])[1]),
                    )
                    tt_range = list(tt_range)
                    sel_timestep += tt_range
                ignore = True

        if "sellevel" in x:
            text = re.compile("sellevel \\(warning\\): level [0-9]* not found")
            all_text = text.findall(x)
            if len(all_text) > 0:
                for tt in all_text:
                    sel_level.append(int(re.findall(r"\d+", all_text[0])[0]))
                ignore = True
        if "grid latitudes differ" in x:
            warnings.warn(
                message="Grid latitudes differ in operation. Check if this is acceptable!"
            )
            ignore = True

        if "grid longitudes differ" in x:
            warnings.warn(
                message="Grid longitudes differ in operation. Check if this is acceptable!"
            )
            ignore = True

        if "found more than one time variable, skipped variable" in x:
            message = x.split("found more than one time variable, skipped variable ")[
                1
            ].replace("!", "")
            warnings.warn(
                message=f"CDO found more than one time variable. Only one is allowed. {message} was skipped"
            )
            ignore = True

        if "Using constant grid cell area weights!" in x:
            warnings.warn(
                message="Using constant grid cell area weights! If you need weighted cell areas, please fix the dataset grid!"
            )
            ignore = True

        if "selmonth" in x:
            text = re.compile("selmonth \\(warning\\): month [0-9]* not found")
            all_text = text.findall(x)
            if len(all_text) > 0:
                for tt in all_text:
                    sel_month.append(int(re.findall(r"\d+", all_text[0])[0]))
                ignore = True
        if "warning" in x:
            text = re.compile("variable name .* not found")
            if len(text.findall(x)) > 0:
                for y in text.findall(x):
                    sel_var.append(y.split("variable name ")[1].split(" ")[0])
                ignore = True

        if not ignore:
            if "warning" in x and "vertmean" in x:
                if "layer bounds not available, using constant vertical weights" in x:
                    warnings.warn(
                        "Layer bounds not available in netCDF file, using constant vertical weights for vertical mean"
                    )
                    warned = True

            if "warning" in x:
                if (
                    "Grid cell bounds not available, using constant grid cell area weights"
                    in x
                ):
                    warnings.warn(
                        "CDO warning: Grid cell bounds not available, using constant grid cell area weights for operation"
                    )
                    warned = True

            if "warning" in x:
                if (
                    "Computation of grid cell area weights failed, grid cell center and bounds coordinates missing"
                    in x
                ):
                    warnings.warn(
                        "CDO warning: Computation of grid cell area weights failed, grid cell center and bounds coordinates missing from netCDF"
                    )
                    warned = True
            if "warning" in x:
                if (
                    "fldmean (warning): grid cell bounds not available, using constant grid cell area weights"
                    in x
                ):
                    warnings.warn(
                        "Grid cell bounds are not available. Constant grid cell weights are used for spatial mean!"
                    )
                    warned = True
            if "warning" in x:
                text = re.compile(
                    "unknown units \[.*\] supplied for grid cell corner .*; proceeding assuming .*!"
                )
                text_find = text.findall(x)
                if len(text_find) > 0:
                    message = text_find[0]
                    message = "Warning for grid area calculations: " + message
                    warnings.warn(message)
                    warned = True

                text = re.compile(
                    "delete \(warning\): timestep .* not found"
                )
                text_find = text.findall(x)
                if len(text_find) > 0:
                    message = text_find[0]
                    message = "Warning: attempting to drop non-existent timesteps!"
                    warnings.warn(message)
                    warned = True

            ## Unsupported array structure message
            if "unsupported" in x and "skipped variable" in x:
                text = re.compile("skipped variable .*!")
                bad_var = (
                    text.findall(x)[0]
                    .split(" ")[2]
                    .replace("!", "")
                )
                message = f"This variable's structure is not supported by CDO: {bad_var}. Full CDO warning: {x}"
                warnings.warn(message)
                warned = True

            if "warning" in x:
                if "day 29feb not found" in x:
                    warnings.warn("No leap years found in data!")
                    warned = True

            text = re.compile(
                "grids have different types! first grid: .*; second grid: .*"
            )
            checks = text.findall(x)
            if len(checks) > 0:
                i_out = checks[0].replace("grids have", "Grids have")
                warnings.warn(i_out)
                warned = True

            if "warning" in x:
                if "input parameters have different levels!" in x:
                    warnings.warn("Input parameters have different levels!")
                    warned = True

            if not warned:
                if "arning" in x:
                    warnings.warn(f"CDO warning: {x}")
    if len(drop_warnings) > 0:
        message = ",".join(drop_warnings)
        message = f"The following months do not exist in the dataset: {message}"
        warnings.warn(message)

    if len(sel_timestep) > 0:
        len_sel = len(sel_timestep)
        # first, figure out if this is a timestep range
        if set(range(min(sel_timestep), max(sel_timestep) + 1)) == set(sel_timestep):
            sel_timestep = [x for x in sel_timestep]
            if len(sel_timestep) > 1:
                sel_timestep = str(min(sel_timestep)) + "-" + str(max(sel_timestep))
            else:
                sel_timestep = str(sel_timestep[0])
        else:
            sel_timestep = ",".join([str(x) for x in sel_timestep])
        if len_sel > 1:
            message = f"{len_sel} timesteps were missing in the dataset: {sel_timestep}"
        else:
            message = (
                f"The following timestep was missing in the dataset: {sel_timestep}"
            )
        warnings.warn(message=message)

    if len(sel_level) > 0:
        len_sel = len(sel_level)
        # first, figure out if this is a level range
        if set(range(min(sel_level), max(sel_level) + 1)) == set(sel_level):
            if len(sel_level) > 1:
                sel_level = str(min(sel_level)) + "-" + str(max(sel_level))
            else:
                sel_level = str(sel_level[0])
        else:
            sel_level = ",".join([str(x) for x in sel_level])
        if len_sel > 1:
            message = f"{len_sel} levels were missing in the dataset: {sel_level}"
        else:
            message = f"The following level was missing in the dataset: {sel_level}"
        warnings.warn(message=message)

    if len(sel_day) > 0:
        len_sel = len(sel_day)
        # first, figure out if this is a day range
        if set(range(min(sel_day), max(sel_day) + 1)) == set(sel_day):
            if len(sel_day) > 1:
                sel_day = str(min(sel_day)) + "-" + str(max(sel_day))
            else:
                sel_day = str(sel_day[0])
        else:
            sel_day = ",".join([str(x) for x in sel_day])
        if len_sel > 1:
            message = f"{len_sel} days were missing in the dataset: {sel_day}"
        else:
            message = f"The following day was missing in the dataset: {sel_day}"
        warnings.warn(message=message)

    if len(sel_hour) > 0:
        len_sel = len(sel_hour)
        # first, figure out if this is a hour range
        if set(range(min(sel_hour), max(sel_hour) + 1)) == set(sel_hour):
            if len(sel_hour) > 1:
                sel_hour = str(min(sel_hour)) + "-" + str(max(sel_hour))
            else:
                sel_hour = str(sel_hour[0])
        else:
            sel_hour = ",".join([str(x) for x in sel_hour])
        if len_sel > 1:
            message = f"{len_sel} hours were missing in the dataset: {sel_hour}"
        else:
            message = f"The following hour was missing in the dataset: {sel_hour}"
        warnings.warn(message=message)
    if len(sel_var) > 0:
        sel_var = ",".join(sel_var)
        message = f"The following variables were missing in the dataset: {sel_var}"
        warnings.warn(message)

    if len(sel_year) > 0:
        len_sel = len(sel_year)
        # first, figure out if this is a year range
        if set(range(min(sel_year), max(sel_year) + 1)) == set(sel_year):
            if len(sel_year) > 1:
                sel_year = str(min(sel_year)) + "-" + str(max(sel_year))
            else:
                sel_year = str(sel_year[0])
        else:
            sel_year = ",".join([str(x) for x in sel_year])
        if len_sel > 1:
            message = f"{len_sel} years were missing in the dataset: {sel_year}"
        else:
            message = f"The following year was missing in the dataset: {sel_year}"
        warnings.warn(message=message)

    if len(sel_month) > 0:
        len_sel = len(sel_month)
        # first, figure out if this is a month range
        if set(range(min(sel_month), max(sel_month) + 1)) == set(sel_month):
            if len(sel_month) > 1:
                sel_month = str(min(sel_month)) + "-" + str(max(sel_month))
            else:
                sel_month = str(sel_month[0])
        else:
            sel_month = ",".join([str(x) for x in sel_month])
        if len_sel > 1:
            message = f"{len_sel} months were missing in the dataset: {sel_month}"
        else:
            message = f"The following month was missing in the dataset: {sel_month}"
        warnings.warn(message=message)

    return target


def run_this(os_command, self, output="one", out_file=None, suppress=False):
    from tqdm import tqdm

    if len(self) == 0:
        raise ValueError("Failure do to empty dataset!")

    self._ncommands += 1

    cores = session_info["cores"]

    if len(self) == 1:
        output = "ensemble"

    if self._execute is False:
        if len(self._hold_history) == len(self.history):
            self.history.append(os_command)
        else:
            self.history[-1] = os_command + " " + self.history[-1].replace("cdo ", " ")
            self.history[-1] = self.history[-1].replace("  ", " ")
    try:
        if self._execute:

            if ((output == "ensemble") and (len(self) > 1)) or (
                (output == "ensemble") and (len(self) == 1)
            ):
                new_history = copy.deepcopy(self._hold_history)

                if len(self) == 1:
                    cores = 1
                file_list = self.current

                if len(self.history) > len(self._hold_history):
                    os_command = f'{os_command} {self.history[-1].replace("cdo ", " ")}'
                    os_command = os_command.replace("  ", " ")

                if cores > 1:
                    original_sigint_handler = signal.signal(
                        signal.SIGTERM, signal.SIG_IGN
                    )
                    pool = multiprocessing.Pool(cores)
                    signal.signal(signal.SIGTERM, original_sigint_handler)

                    target_list = []
                    results = dict()
                else:
                    target_list = []

                progress_bar = False

                if self._thredds is False:
                    if self.size["Number of files in ensemble"] >= 12:
                        if self.size["Ensemble size"].split(" ")[1] == "GB":
                            if float(self.size["Ensemble size"].split(" ")[0]) > 12:
                                progress_bar = True

                if session_info["progress"] == "off":
                    progress_bar = False

                if session_info["progress"] == "on" and len(self) > 1:
                    progress_bar = True

                if cores == 1:
                    if progress_bar:
                        if session_info["progress"] == "on":
                            if not suppress:
                                print("Processing ensemble! In progress:")
                        else:
                            if not suppress:
                                print("Processing large ensemble! In progress")
                        if not suppress:
                            pbar = tqdm(total=len(file_list), position=0, leave=True)

                for ff in file_list:
                    ff_command = os_command

                    ff_command = f"{ff_command} {ff} "
                    if "infile09178" in ff_command:
                        ff_command = " ".join(ff_command.split(" ")[:-2])
                        ff_command = ff_command.replace("infile09178", ff)

                    target = temp_file("nc")

                    if out_file is not None:
                        target = out_file

                    ff_command = f"{ff_command} {target}"
                    ff_command = ff_command.replace("  ", " ")
                    if " --sortname " in os_command:
                        os_command = os_command.replace(" --sortname ", " ")
                        os_command = os_command.replace("cdo  ", "cdo --sortname ")

                    if "reduce_dim" in ff_command:
                        ff_command = (
                            ff_command.replace("reduce_dim", "")
                            .replace(" - ", " ")
                            .replace(" -- ", " ")
                        )
                        ff_command = ff_command.replace("cdo ", "cdo --reduce_dim ")

                    ff_command = tidy_command(ff_command)

                    zip_copy = False
                    if self._zip and self._ncommands == 1:
                        zip_copy = True

                    format_it = False
                    if self._format is not None:
                        format_it = True
                        if self._ncommands == 1:
                            ff_command = ff_command.replace(
                                "cdo ", f"cdo -f {self._format} copy "
                            )
                        else:
                            ff_command = ff_command.replace(
                                "cdo ", f"cdo -f {self._format} "
                            )
                    ff_command = ff_command.replace(
                        "cdo ", f"cdo {self._align} "
                    ).replace("  ", " ")

                    if self._zip and zip_copy and format_it is False:
                        ff_command = ff_command.replace("cdo ", "cdo -z zip copy ")
                    else:
                        if self._zip:
                            ff_command = ff_command.replace("cdo ", "cdo -z zip ")

                    new_history.append(ff_command)

                    if cores > 1:
                        temp = pool.apply_async(
                            run_cdo,
                            [ff_command, target, out_file, False, self._precision],
                        )
                        results[ff] = temp
                    else:

                        target = run_cdo(
                            ff_command, target, out_file, precision=self._precision
                        )
                        target_list.append(target)
                        if progress_bar:
                            if not suppress:
                                pbar.update(1)

                if cores > 1:

                    if progress_bar:
                        if session_info["progress"] == "on":
                            if not suppress:
                                print("Processing ensemble. In progress:")
                        else:
                            if not suppress:
                                print("Processing a large ensemble. In progress:")
                        if not suppress:
                            pbar = tqdm(total=len(file_list), position=0, leave=True)
                    for k, v in results.items():
                        target_list.append(v.get())
                        if progress_bar:
                            if not suppress:
                                pbar.update(1)

                self.history = copy.deepcopy(new_history)
                self.current = copy.deepcopy(target_list)

                if cores == 1 or session_info["parallel"]:
                    for ff in target_list:
                        remove_safe(ff)

                self.disk_clean()

                cleanup()

                self._hold_history = copy.deepcopy(self.history)

                self._zip = False

                self._ncommands = 0

                self._format = None

                return None

            if ((output == "one") and (len(self) > 1)) or self._zip is False:

                new_history = copy.deepcopy(self._hold_history)

                if len(self.history) > len(self._hold_history):
                    os_command = f'{os_command} {self.history[-1].replace("cdo ", " ")}'
                    os_command = os_command.replace("  ", " ")

                # ensure there is sufficient space in /tmp if it is to be used
                if platform.system() == "Linux":
                    all_sizes = 0

                    for ff in self:
                        if file_size(ff) is not None:
                            all_sizes += file_size(ff)

                    result = os.statvfs("/tmp/")
                    result = result.f_frsize * result.f_bavail

                    if result < (2 * all_sizes):
                        session_info["temp_dir"] == "/var/tmp/"

                target = temp_file("nc")

                if out_file is not None:
                    target = out_file

                os_command = (
                    os_command + " [ " + str_flatten(self.current, " ") + " ] " + target
                )

                zip_copy = False
                if self._zip and self._ncommands == 1:
                    zip_copy = True

                format_it = False

                if self._format is not None:
                    format_it = True
                    if self._ncommands == 1:
                        os_command = os_command.replace(
                            "cdo ", f"cdo -f {self._format} copy "
                        )
                    else:
                        os_command = os_command.replace(
                            "cdo ", f"cdo -f {self._format} "
                        )

                if self._zip and zip_copy and format_it is False:
                    os_command = os_command.replace("cdo ", "cdo -z zip copy ")
                else:
                    if self._zip:
                        os_command = os_command.replace("cdo ", "cdo -z zip ")

                if "infile09178" in os_command:
                    os_command = os_command.replace(ff, "")
                    os_command = os_command.replace("infile09178", ff)

                os_command = tidy_command(os_command)

                os_command = os_command.replace("cdo ", f"cdo {self._align} ").replace(
                    "  ", " "
                )

                if "mergetime" in os_command:
                    try:
                        target = run_cdo(
                            os_command, target, out_file, precision=self._precision
                        )
                    except:

                        var_list = []
                        var_com = []

                        for ff in self:
                            var_list += nc_variables(ff)
                            var_com.append(nc_variables(ff))
                        new_list = []

                        for var in set(var_list):
                            if len(var_com) == len([x for x in var_com if var in x]):
                                new_list.append(var)
                        if version_below(session_info["cdo"], "1.9.9"):

                            target = run_cdo(
                                os_command, target, out_file, precision=self._precision
                            )
                        else:
                            f_list = ",".join(new_list)
                            os_command = os_command.replace(
                                "-mergetime ", f'-mergetime -apply,"-selname,{f_list}" '
                            )

                            removed = ",".join(
                                [x for x in set(var_list) if x not in new_list]
                            )
                            if len([x for x in set(var_list) if x not in new_list]) > 0:
                                warnings.warn(
                                    f"The following variables are not in all files, so were ignored when merging: {removed}"
                                )

                            target = run_cdo(
                                os_command, target, out_file, precision=self._precision
                            )
                else:
                    target = run_cdo(
                        os_command, target, out_file, precision=self._precision
                    )

                remove_safe(target)

                self.current = target

                self.history = new_history
                self.history.append(os_command)

                self.disk_clean()

                cleanup()

                self._hold_history = copy.deepcopy(self.history)

                self._zip = False
                self._n_commands = 0

                self._format = None
    except Exception as e:
        self.reset()
        raise ValueError(e)
