
import copy
import os
import re
import subprocess
import platform
import warnings

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

def ann_anomaly(
    ff, baseline, metric, window, align, precision, new_files, new_commands, nc_safe):
    """
    Function to calculate the anomaly for a single file
    """
    # throw error if baseline is not valid
    orig_safe = copy.deepcopy(nc_safe)
    target = temp_file("nc")
    nc_safe.append(target)
    try:

        # create the target file
        # generate the cdo command
        if metric == "absolute":
            cdo_command = (
                f"cdo -sub -runmean,{window} -yearmean {ff} -timmean "
                f"-selyear,{baseline[0]}/{baseline[1]} {ff} {target}"
            )
        else:
            cdo_command = (
                f"cdo -div -runmean,{window} -yearmean {ff} -timmean "
                f"-selyear,{baseline[0]}/{baseline[1]} {ff} {target}"
            )

        # run the command and save the temp file

        cdo_command = tidy_command(cdo_command)
        cdo_command = cdo_command.replace(
            "cdo ", f"cdo --timestat_date {align} "
        ).replace("  ", " ")

        target = run_cdo(cdo_command, target, precision=precision)
        if target not in nc_safe:
            nc_safe.append(target)

        # update the new files and commands
        new_files.append(target)
        new_commands.append(cdo_command)
    except BaseException as e:
        try:
            nc_safe.remove(target)
        except:
            pass
        return e

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
        raise TypeError("Precision must be str")

    if precision not in ["I8", "I16", "I32", "F32", "F64", "default"]:
        raise ValueError(f"Precision - {precision} - is not valid")

    if precision in ["I8", "I16", "I32", "F32", "F64"]:
        if " -b " not in command:
            command = command.replace("cdo ", f"cdo -b {precision} ")

    # make sure the output file does not exist

    command = tidy_command(command)

    if target is None:
        raise TypeError("Target must be specified")

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

    if command.startswith("cdo ") is False:
        raise ValueError("The command does not start with cdo!")

    append_safe(target)

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
            warnings.warn(
                f"None of the months supplied are in one of the dataset files. Please check months supplied to nctoolkit methods, if necessary!"
            )
            return None

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
                for z in re.findall(r"\d+", y):
                    drop_warnings.append(z)
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

                text = re.compile("delete \(warning\): timestep .* not found")
                text_find = text.findall(x)
                if len(text_find) > 0:
                    message = text_find[0]
                    message = "Warning: attempting to drop non-existent timesteps!"
                    warnings.warn(message)
                    warned = True

            ## Unsupported array structure message
            if "unsupported" in x and "skipped variable" in x:
                text = re.compile("skipped variable .*!")
                bad_var = text.findall(x)[0].split(" ")[2].replace("!", "")
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