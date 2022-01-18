import atexit
import glob
import sys
import copy
import multiprocessing as mp
import os
import pandas as pd
import random
import re
import string
import subprocess
import warnings
import urllib.request
import platform

from netCDF4 import Dataset

from nctoolkit.cleanup import cleanup, clean_all, temp_check
from nctoolkit.flatten import str_flatten
from nctoolkit.runthis import run_cdo
from nctoolkit.session import (
    nc_protected,
    nc_protected_par,
    session_info,
    nc_safe,
    append_safe,
    remove_safe,
    append_protected,
    remove_protected,
    append_tempdirs,
)
from nctoolkit.session import nc_safe_par, temp_dirs, nc_protected, temp_dirs_par
from nctoolkit.show import (
    nc_variables,
    nc_years,
    nc_months,
    nc_levels,
    nc_times,
    nc_format,
)
from nctoolkit.temp_file import temp_file


# context manager code so that thredds checks will be stopped if slow
import signal
import time
from contextlib import contextmanager
import xarray as xr


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException(
            "Timed out. Connecting to the thredds server is very slow!"
        )

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


# A custom format for warnings.
def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + "\n"


warnings.formatwarning = custom_formatwarning

# set up the session info
letters = string.ascii_lowercase
session_info["stamp"] = (
    "nctoolkit" + "".join(random.choice(letters) for i in range(8)) + "nctoolkit"
)
session_info["temp_dir"] = "/tmp/"
session_info["user_dir"] = False
session_info["thread_safe"] = False
session_info["lazy"] = True
session_info["precision"] = None
session_info["parallel"] = False

session_info["interactive"] = sys.__stdin__.isatty()


if platform.system() == "Linux":
    result = os.statvfs("/tmp/")
    session_info["size"] = result.f_frsize * result.f_bavail
else:
    session_info["size"] = 0


session_info["latest_size"] = 0
session_info["cores"] = 1

if platform.system() == "Linux":
    append_tempdirs("/tmp")
    append_tempdirs("/var/tmp")


def options(**kwargs):
    """
    Define session options.
    Set the options in the session. Available options are thread_safe and lazy.
    Set thread_safe = True if hdf5 was built to be thread safe.
    Set lazy = True if you want methods to evaluate lazy by default.
    Set cores = n, if you want nctoolkit to process the individual files in multi-file datasets in parallel. Note this
    only applies to multi-file datasets and will not improve performance with single files.
    Set temp_dir = "/foo" if you want to change the temporary directory used by nctoolkit to save temporary files.

    Parameters
    ---------------
    **kwargs
        Define options using key, value pairs.

    Examples
    ------------

    If you wanted to process the files in multi-file datasets in parallel with 6 cores, do the following:

    >>> import nctoolkit as nc
    >>> nc.options(cores = 6)

    If you want to set evaluation to always be lazy do the following:

    >>> nc.options(lazy = True)

    If you want nctoolkit to store temporary files in a specific directory, do this:

    >>> nc.options(temp_dir = "/foo")

    """

    valid_keys = ["thread_safe", "lazy", "cores", "precision", "temp_dir", "parallel"]

    for key in kwargs:
        if key not in valid_keys:
            raise AttributeError(key + " is not a valid option")

        if key == "parallel" or key == "lazy" or key == "thread_safe":
            if type(kwargs[key]) is not bool:
                raise TypeError(f"{key} should be boolean")

        if type(kwargs[key]) is not bool:
            if key == "temp_dir":
                if type(kwargs[key]) is str:
                    if os.path.exists(kwargs[key]) == False:
                        raise ValueError("The temp_dir specified does not exist!")
                    session_info[key] = os.path.abspath(kwargs[key])
                    session_info["user_dir"] = True
                return None

            if key == "cores":
                if type(kwargs[key]) is int:
                    if kwargs[key] > mp.cpu_count():
                        raise ValueError(
                            str(kwargs[key])
                            + " is greater than the number of system cores ("
                            + str(mp.cpu_count())
                            + ")"
                        )
                    session_info[key] = kwargs[key]
                else:
                    raise TypeError("cores must be an int")
            else:
                if key == "precision":
                    if kwargs[key] not in ["I8", "I16", "I32", "F32", "F64"]:
                        raise ValueError("precision supplied is not valid!")
                    session_info[key] = kwargs[key]
                else:
                    raise ValueError(kwargs[key] + " is not valid session info!")
        else:
            session_info[key] = kwargs[key]

            # update safe-lists etc. if running in parallel
            if kwargs[key] and key == "parallel":

                if len(temp_dirs) > 0:
                    for ff in temp_dirs:
                        append_tempdirs(ff)

                if len(nc_safe) > 0:
                    for ff in nc_safe:
                        nc_safe_par.append(ff)

                if len(nc_protected) > 0:
                    for ff in nc_protected:
                        nc_protected_par.append(ff)
                        nc_protected.remove(ff)

            if (kwargs[key] == False) and key == "parallel":

                if len(temp_dirs_par) > 0:
                    for ff in temp_dirs_par:
                        append_tempdirs(ff)

                if len(nc_safe_par) > 0:
                    for ff in nc_safe_par:
                        nc_safe.append(ff)
                        nc_safe_par.remove(ff)

                if len(nc_protected_par) > 0:
                    for ff in nc_protected_par:
                        nc_protected.append(ff)
                        nc_protected_par.remove(ff)


# if nctoolkitrc exists, we need to read the possible options from there...


def find_config():
    # first look in the working directory
    for ff in [".nctoolkitrc", "nctoolkitrc"]:
        if os.path.exists(ff):
            return ff

    # now look in the home directory....
    from os.path import expanduser

    home = expanduser("~")
    for ff in [".nctoolkitrc", "nctoolkitrc"]:
        if os.path.exists(home + "/" + ff):
            return home + "/" + ff

    return None


config_file = find_config()

if config_file is not None:
    valid_keys = ["thread_safe", "lazy", "cores", "precision", "temp_dir"]

    file1 = open(config_file, "r")
    Lines = file1.readlines()

    count = 0
    # Strips the newline character
    for line in Lines:
        text = line.replace(" ", "").strip()
        if text.count(":") != 1:
            raise ValueError(f"Line in {config_file} is invalid: {line}")

    for line in Lines:
        text = line.replace(" ", "").strip()

        terms = text.split(":")

        # three options, all words, boolean or integers

        # set the key

        key = terms[0]
        value = None

        if key not in valid_keys:
            raise ValueError(f"{config_file} is trying to set invalid key: {terms[0]}")

        if (terms[1].strip() == "True") and value is None:
            value = True

        if (terms[1] == "False") and (value is None):
            value = False

        if (terms[1].isnumeric()) and (value is None):
            value = int(terms[1])

        if value is None:
            value = terms[1]
            value = value.replace("'", "").replace('"', "")

        valid_keys = [
            "thread_safe",
            "lazy",
            "cores",
            "precision",
            "user",
            "password",
            "temp_dir",
        ]

        if key not in valid_keys:
            raise ValueError(f"{config_file} is trying to set invalid key: {terms[0]}")

        if key == "temp_dir":
            if type(value) is str:
                if os.path.exists(value) == False:
                    raise ValueError(
                        f"The temp_dir specified by {config_file} does not exist: {value}"
                    )
                session_info[key] = os.path.abspath(value)
                session_info["user_dir"] = True

        if key == "cores":
            if type(value) is int:
                if value > mp.cpu_count():
                    raise ValueError(
                        str(value)
                        + " is greater than the number of system cores ("
                        + str(mp.cpu_count())
                        + ")"
                    )
                session_info[key] = value
            else:
                raise TypeError("cores must be an int")

        if key == "precision":
            if value not in ["I8", "I16", "I32", "F32", "F64"]:
                raise ValueError("precision supplied is not valid!")
            session_info[key] = value

        if key in ["thread_safe", "lazy"]:
            if type(value) == bool:
                session_info[key] = value
            else:
                raise ValueError(f"{key} must be boolean!")

        if key in ["user", "password"]:
            if type(value) is not str:
                raise ValueError(f"{key} must be str!")
            else:
                session_info[key] = value


# register clean_all to clean temp files on exit
atexit.register(clean_all)

# run temp_check to see if any files are held over from previous sessions
temp_check()


def is_url(x):
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return re.match(regex, x) is not None


def convert_bytes(num):
    """
    A function to make file size human readable
    """
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < 1000.0:
            return str(num) + " " + x
        num /= 1000.0


def file_size(file_path):
    """
    A function to return file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size


def from_xarray(ds):

    """
    Convert an xarray dataset to an nctoolkit dataset
    This will first save the xarray dataset as a temporary netCDF file.

    Parameters
    ---------------
    ds : xarray dataset
    ---------------
    from_xarray : nctoolkit.DataSet
    """
    ff = temp_file(".nc")
    ds.to_netcdf(ff)

    append_safe(ff)

    d = DataSet(ff)
    return d


def open_data(x=[], checks=False, **kwargs):
    """
    Read netCDF data as a DataSet object

    Parameters
    ---------------
    x : str or list
        A string or list of netCDF files or a single url. The function will check the
        files exist. If x is not a list, but an iterable it will be converted to a list.
        If a *.nc style wildcard is supplied, open_data will use all files available.
        By default an empty dataset is created, ie. using open_data() will create an empty
        dataset that can then be expanded using append.
    checks: boolean
        Do you want basic checks to ensure cdo can read files?
    **kwargs: kwargs
        Optional arguments for internal use by open_thredds and open_url.

    Returns
    ---------------
    open_data : nctoolkit.DataSet


    Examples
    ------------

    If you want to open a single file as a dataset, do the following:

    >>> import nctoolkit as nc
    >>> ds = nc.open_data("example.nc")

    If you want to open a list of files as a multi-file dataset, you would do something like this:

    >>> import nctoolkit as nc
    >>> ds = nc.open_data(["file1.nc", "file2.nc", "file3.nc"])

    If you wanted to open all files in a directory "data" as a multi-file dataset, you can use a wildcard:

    >>> import nctoolkit as nc
    >>> ds = nc.open_data("data/*.nc")

    """
    # from nctoolkit.temp_file import temp_file

    if type(x) is str:
        if x.endswith("*.nc"):
            x = glob.glob(x)

    thredds = False

    ftp_details = None
    wait = None
    file_stop = None

    source = "file"

    for key in kwargs:
        if key == "thredds":
            thredds = kwargs[key]
        if key == "ftp_details":
            ftp_details = kwargs[key]
        if key == "wait":
            wait = kwargs[key]
        if key == "file_stop":
            file_stop = kwargs[key]
        if key == "source":
            source = kwargs[key]

    # make sure data has been supplied
    if x is None:
        raise ValueError("No data was supplied!")

    # coerce an iterable to a list
    if type(x) is not str:
        x = [y for y in x]
        for ff in x:
            if type(ff) is not str:
                raise TypeError("You have not supplied an iterable made of file paths!")

    if type(x) is list:
        if len(x) == 1:
            x = x[0]

    # check the files provided exist
    stop_time = 10000000000000000000000000000000000
    if wait is not None:
        stop_time = min(wait, stop_time)
    if file_stop is not None:
        stop_time = min(file_stop, stop_time)

    if type(x) is str:
        ##if os.path.exists(x) is False:
        if source != "file" or os.path.exists(x) is False:

            if is_url(x):

                if thredds is False:
                    new_x = temp_file(".nc")
                    print(f"Downloading {x}")
                    print("\033[A                             \033[A")

                    if ftp_details is not None and x.startswith("ftp"):
                        user = ftp_details["user"]
                        password = ftp_details["password"]
                        x = x.replace("ftp://", f"ftp://{user}:{password}@")

                    start = time.time()

                    i = 0

                    search = True
                    while search:
                        if os.path.exists(new_x) == False:
                            try:
                                # work out if there is a time limit for individual files
                                if stop_time != 10000000000000000000000000000000000:
                                    with time_limit(stop_time):
                                        urllib.request.urlretrieve(x, new_x)
                                else:
                                    urllib.request.urlretrieve(x, new_x)
                            except:
                                nothing = "x"
                        search += 1
                        if os.path.exists(new_x):
                            break

                        if wait is None:
                            if search == 3:
                                break
                        else:
                            end = time.time()
                            if (end - start) > wait:
                                break
                    if os.path.exists(new_x) == False:
                        raise ValueError(f"Could not download {x}")

                    x = new_x
                else:

                    if checks:
                        if wait is not None:
                            with time_limit(stop_time):
                                out = subprocess.run(
                                    "cdo sinfo " + x,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                )
                                if "Open failed" in str(out.stderr):
                                    raise ValueError(f"{x} is not compatible with CDO!")

            else:
                raise FileNotFoundError("Data set " + x + " does not exist!")

        if checks:
            out = subprocess.run(
                "cdo sinfo " + x,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if "Open failed" in out.stderr.decode("utf-8"):
                mes = (
                    out.stderr.decode("utf-8")
                    .replace("cdo    sinfo: ", "")
                    .replace("<\n", "")
                    .replace("\n", "")
                )
                mes = re.sub(" +", " ", mes)
                raise ValueError(mes)

        else:
            append_safe(x)
            append_protected(x)

    # it's possible there are duplicates in the data
    # Get rid of them..
    # Note: This will also ensure the original list is deep copied

    if type(x) is list:
        orig_size = len(x)
        x = list(dict.fromkeys(x))
        if len(x) < orig_size:
            warnings.warn(message="Duplicates in data set have been removed!")

    if type(x) is list:
        if source == "url":

            for ff in x:

                if is_url(ff) == False:
                    raise ValueError(f"{x} is not a url")

            new_files = []
            for ff in x:

                if is_url(ff):

                    if thredds is False:
                        new_x = temp_file(".nc")
                        print(f"Downloading {ff}")
                        print("\033[A                             \033[A")

                        if ftp_details is not None and x.startswith("ftp"):
                            user = ftp_details["user"]
                            password = ftp_details["password"]
                            ff = ff.replace("ftp://", f"ftp://{user}:{password}@")

                        start = time.time()

                        i = 0

                        search = True
                        while search:
                            if os.path.exists(new_x) == False:
                                try:
                                    # work out if there is a time limit for individual files
                                    if stop_time != 10000000000000000000000000000000000:
                                        with time_limit(stop_time):
                                            urllib.request.urlretrieve(ff, new_x)
                                    else:
                                        urllib.request.urlretrieve(ff, new_x)
                                except:
                                    nothing = "x"
                            search += 1
                            if os.path.exists(new_x):
                                break

                            if wait is None:
                                if search == 3:
                                    break
                            else:
                                end = time.time()
                                if (end - start) > wait:
                                    break
                        if os.path.exists(new_x) == False:
                            raise ValueError(f"Could not download {x}")

                        new_files.append(new_x)
                x = new_files

    if type(x) is list and source != "url":
        if thredds is False:

            for ff in x:
                if os.path.exists(ff) is False:
                    raise FileNotFoundError(f"{ff} does not exist!")
            for ff in x:
                append_safe(ff)
                append_protected(ff)

            if len(x) > 1:
                for ff in x:

                    if os.path.exists(ff) is False:
                        raise FileNotFoundError("Data set " + ff + " does not exist!")

    # if there is only one file in the list, change it to a single file
    if type(x) is list:
        if len(x) == 1:
            x = x[0]

    d = DataSet(x)
    d._thredds = thredds

    if len(d) == 1:
        df = d.contents.reset_index(drop=True).query("'I' in data_type")
        if len(df) > 0:
            check = ",".join(list(df.variable))
            if "," in check:
                warnings.warn(
                    message=f"The variable(s) {check} have integer data type. Consider setting data type to float 'F64' or 'F32' using set_precision."
                )
            else:
                warnings.warn(
                    message=f"The variable {check} has integer data type. Consider setting data type to float 'F64' or 'F32' using set_precision."
                )

    return d


def open_thredds(x=None, wait=None, checks=False):
    """
    Read thredds data as a DataSet object

    Parameters
    ---------------
    x : str or list
        A string or list of thredds urls, which must end with .nc.
    checks : boolean
        Do you want to check if data is available over thredds?
    wait : int
        Time to wait for thredds server to be checked. Limitless if not supplied.

    Returns
    ---------------
    open_thredds : nctoolkit.DataSet

    Examples
    ------------

    If you want to open a file available over thredds or opendap, do the following:

    >>> import nctoolkit as nc
    >>> ds = nc.open_thredds("htttp:://foo.nc")


    """

    if type(checks) is not bool:
        raise TypeError("Please provide boolean for checks")

    if wait is not None:
        if type(wait) is not int and float:
            raise TypeError("Please provide an integer for wait!")
        if wait <= 0:
            raise ValueError("Please provide a positive value for wait!")

    if session_info["cores"] > 1:
        warnings.warn(
            message="Using multiple cores on thredds data is volatile. It has therefore been reset to 1."
        )
        session_info["cores"] = 1

    return open_data(x=x, thredds=True, wait=wait, checks=checks, source="thredds")


def open_url(x=None, ftp_details=None, wait=None, file_stop=None):
    """
    Read netCDF data from a url as a DataSet object

    Parameters
    ---------------
    x : str
        A string with a url. Prior to processing data will be downloaded to
        a temp folder.
    ftp_details : dict
        A dictionary giving the user name and password combination for ftp downloads: {"user":user, "password":pass}
    wait : int
        Time to wait, in seconds, for data to download. A minimum of 3 attempts will be made to download the data.
    file_stop : int
        Time limit, in minutes, for individual attempts at downloading data. This is useful to get around download freezes.

    Returns
    ---------------
    open_url : nctoolkit.DataSet

    Examples
    ------------

    If you want to open a file available over a url do the following:

    >>> import nctoolkit as nc
    >>> ds = nc.open_url("htttp:://foo.nc")

    This will download the file as a temporary folder for use in the dataset.

    """

    if wait is not None:
        if type(wait) is not int:
            raise TypeError("Please provide a valid wait!")

        if wait <= 0:
            raise TypeError("Please provide a valid wait!")

    if file_stop is not None:
        if type(file_stop) is not int:
            raise TypeError("Please provide a valid file_stop!")

        if file_stop <= 0:
            raise TypeError("Please provide a valid file_stop!")

    if ftp_details is not None:
        if len(ftp_details) != 2:
            raise ValueError("ftp_details is not a 2 element dictionary")

        user = ftp_details[list(ftp_details.keys())[0]]
        password = ftp_details[list(ftp_details.keys())[1]]
        new_dict = {"user": user, "password": password}
    else:
        new_dict = None

    return open_data(
        x=x, ftp_details=new_dict, wait=wait, file_stop=file_stop, source="url"
    )


def merge(*datasets, match=["day", "year", "month"]):
    """
    Merge datasets

    Parameters
    -------------
    datasets: kwargs
        Datasets to merge.
    match: list
        Temporal matching criteria. This is a list which must be made up of a subset of
        day, year, month. This checks that the datasets have compatible times.
        For example, if you want to ensure the datasets have the same years, then use
        match = ["year"].
    """
    all_files = []
    for dataset in datasets:
        if ("DataSet" in str(type(dataset))) is False:
            raise TypeError("Please check everything is a DataSet object!")
        # make sure everything has been evaluated
        dataset.run()
        all_files += dataset.current
    result = open_data(all_files)
    result.merge(match=match)
    return result


def cor_time(x=None, y=None):
    """
    Calculate the temporal correlation coefficient between two datasets
    This will calculate the temporal correlation coefficient, for each time step,
    between two datasets. The datasets must either have the same variables or only
    have one variable.

    Parameters
    -------------
    x: dataset
        First dataset to use
    y: dataset
        Second dataset to use
    """

    if ("DataSet" in str(type(x))) is False:
        raise TypeError("Please check x is a dataset")

    if ("DataSet" in str(type(y))) is False:
        raise TypeError("Please check y is a dataset")
        # make sure everything has been evaluated

    x.run()
    y.run()

    if len(x) > 1 or len(y) > 1:
        raise TypeError("cor_time only accepts single file datasets!")

    a = x.copy()
    b = y.copy()

    if x.variables != y.variables:
        if len(x.variables) > 1 or len(y.variables) > 1:
            raise ValueError(
                "This method currently only works with single variable datasets or "
                "datasets with identical variables!"
            )

    target = temp_file("nc")

    if len(x.variables) == 1:
        command = (
            "cdo -setname,cor -timcor "
            + a.current[0]
            + " "
            + b.current[0]
            + " "
            + target
        )
    else:
        command = "cdo -timcor " + a.current[0] + " " + b.current[0] + " " + target

    target = run_cdo(command, target=target, precision=x._precision)

    data = open_data(target)

    remove_safe(target)

    return data


def cor_space(x=None, y=None):
    """
    Calculate the spatial correlation coefficient between two datasets
    This will calculate the spatial correlation coefficient, for each time step,
    between two datasets. The datasets must either have the same variables or only
    have one variable.

    Parameters
    -------------
    x: dataset
        First dataset to use
    y: dataset
        Second dataset to use
    """

    if ("DataSet" in str(type(x))) is False:
        raise TypeError("Please check x is a dataset")

    if ("DataSet" in str(type(y))) is False:
        raise TypeError("Please check y is a dataset")
        # make sure everything has been evaluated

    x.run()
    y.run()

    if len(x) > 1 or len(y) > 1:
        raise TypeError("cor_time only accepts single file datasets!")

    a = x.copy()
    b = y.copy()

    if x.variables != y.variables:
        if len(x.variables) > 1 or len(y.variables) > 1:
            raise ValueError(
                "This method currently only works with single variable datasets "
                "or datasets with identical variables!"
            )

    target = temp_file("nc")

    if len(x.variables) == 1:
        command = (
            "cdo -setname,cor -fldcor "
            + a.current[0]
            + " "
            + b.current[0]
            + " "
            + target
        )
    else:
        command = "cdo -fldcor " + a.current[0] + " " + b.current[0] + " " + target

    target = run_cdo(command, target=target, precision=x._precision)

    data = open_data(target)

    remove_safe(target)

    return data


class DataSet(object):
    """
    A modifiable ensemble of netCDF files
    """

    def __init__(self, start=""):
        """Initialize the starting file name etc"""
        # Attribuates of interest to users
        self.history = []
        self.start = start
        if type(start) is str:
            self._current = [start]
        else:
            self._current = start

        # attributes to the module, but not users (probably)
        if session_info["lazy"]:
            self._execute = False
        else:
            self._execute = True
        self._hold_history = []
        self._merged = False
        self._safe = []
        # some trackers to make end of the chain processing easier
        self._thredds = False
        self._zip = False
        self._format = None

        self._precision = "default"

        self._grid = None
        self._weights = None
        # track number of held over commands
        self._ncommands = 0

    def __getitem__(self, index):

        return self.current[index]

    def __len__(self):
        return len(self.current)

    def __iter__(self):
        for ff in self.current:
            yield ff
        return

    def __repr__(self):
        current = str(len(self)) + " member ensemble"

        variables = []
        for ff in self:
            for vv in nc_variables(ff):
                if vv not in variables:
                    variables.append(vv)

        return (
            "<nctoolkit.DataSet>:\nFiles: "
            + current
            + "\n"
            + "Variables: "
            + str_flatten(variables)
        )

    @property
    def size(self):
        """The size of an object
        This will print the number of files, total size, and smallest and largest files
        in an DataSet object.
        """
        all_sizes = []

        smallest_file = ""
        largest_file = ""
        min_size = 1e15
        max_size = -1

        for ff in self:

            all_sizes.append(file_size(ff))

            if file_size(ff) > max_size:
                max_size = file_size(ff)
                largest_file = ff

            if file_size(ff) < min_size:
                min_size = file_size(ff)
                smallest_file = ff

        min_size = convert_bytes(min_size)
        max_size = convert_bytes(max_size)

        sum_size = convert_bytes(sum(all_sizes))
        result = "Number of files in ensemble: " + str(len(self)) + "\n"
        result = result + "Ensemble size: " + sum_size + "\n"
        result = (
            result + "Smallest file: " + smallest_file + " has size " + min_size + "\n"
        )
        result = result + "Largest file: " + largest_file + " has size " + max_size
        return result

    @property
    def variables(self):
        """
        List variables contained in a dataset
        """

        all_variables = []
        for ff in self:
            all_variables += nc_variables(ff)

        all_variables = list(set(all_variables))

        all_variables.sort()

        return all_variables

    @property
    def months(self):
        """
        List months contained in a dataset
        """

        all_months = []
        for ff in self:
            all_months += nc_months(ff)

        all_months = list(set(all_months))

        all_months.sort()

        return all_months

    @property
    def levels(self):
        """
        List levels contained in a dataset
        """

        all_levels = []
        for ff in self:
            all_levels += nc_levels(ff)

        all_levels = list(set(all_levels))

        all_levels.sort()

        return all_levels

    @property
    def times(self):
        """
        List times contained in a dataset
        """

        all_times = []
        for ff in self:
            all_times += nc_times(ff)

        all_times = list(set(all_times))

        all_times.sort()

        return all_times

    @property
    def ncformat(self):
        """
        List formats of files contained in a dataset
        """

        all_formats = []
        for ff in self:
            all_formats += nc_format(ff)

        all_formats = list(set(all_formats))

        all_formats.sort()

        return all_formats

    @property
    def years(self):
        """
        List years contained in a dataset
        """

        all_years = []
        for ff in self:
            all_years += nc_years(ff)

        all_years = list(set(all_years))

        all_years.sort()

        return all_years

    @property
    def contents(self):
        """
        Detailed list of variables contained in a dataset.
        This will only display the variables in the first file of an ensemble.
        """

        list_contents = []

        use_names = True

        for ff in self:
            if "nctoolkit" in ff:
                use_names = False

        for ff in self:

            dataset = Dataset(ff)

            out = subprocess.run(
                "cdo sinfon " + ff,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if "Unsupported file structure" in str(out.stderr):
                for ff in self:
                    remove_safe(ff)
                    remove_protected(ff)
                raise ValueError("Unsupported file structure")
            if "expandWildCards" in out.stderr.decode("utf-8"):
                for ff in self:
                    remove_safe(ff)
                    remove_protected(ff)
                raise ValueError(out.stderr.decode("utf-8"))
            out = out.stdout.decode("utf-8")
            out = out.split("\n")
            out_inc = ["Grid coordinates :" in ff for ff in out]
            var_det = []
            i = 1
            while True:
                if out_inc[i]:
                    break
                i += 1
                var_det.append(out[i - 1])

            def split_var(x):
                x = x.replace(":", "").split(" ")
                x = [x for x in x if len(x) > 0]
                new_x = []
                include = False
                for y in x[1:]:
                    if y.isnumeric():
                        include = True

                    if include:
                        new_x.append(y)
                return new_x

            def fix_head(x):
                x = (
                    x.replace(":", "")
                    .replace("  ", " ")
                    .replace("Parameter name", "variable")
                )
                x = x[x.find("Level") :].replace("  ", " ")
                return x.split(" ")

            def fix_type(x):
                position = [m.start() for m in re.finditer(":", x)][-1]

                return (
                    x[: (position - 4)]
                    + x[(position - 4) : position].replace(" ", "")
                    + " "
                    + x[(position):]
                )

            var_det[0] = fix_head(var_det[0])
            for ii in range(1, len(var_det)):
                var_det[ii] = fix_type(var_det[ii])
                var_det[ii] = split_var(var_det[ii])

            df = pd.DataFrame.from_records(var_det[1:], columns=var_det[0])
            df = df.loc[:, ["Levels", "Points", "variable", "Dtype"]]
            df = df.rename(
                columns={"Levels": "nlevels", "Points": "npoints", "Dtype": "data_type"}
            )

            longs = None
            units = None
            longs = []

            cdo_result = list(df.variable)

            for x in cdo_result:
                try:
                    longs.append(dataset.variables[x].long_name)
                except:
                    longs.append(None)
            units = []
            for x in cdo_result:
                try:
                    units.append(dataset.variables[x].units)
                except:
                    units.append(None)

            df = pd.DataFrame({"variable": cdo_result}).merge(df)

            if longs is not None:
                df["long_name"] = longs
            if units is not None:
                df["unit"] = units

            df = df.assign(nlevels=lambda x: x.nlevels.astype("int")).assign(
                npoints=lambda x: x.npoints.astype("int")
            )

            times = []

            ds = Dataset(ff)
            time_name = [x for x in ds.variables if "time" in x]

            # get time name

            if len(time_name) > 0:
                time_name = time_name[0]
            else:
                time_name = "time"

            for vv in cdo_result:
                done = False
                try:
                    ds_times = ds[vv][time_name].values
                except:
                    times.append(None)
                    done = True

                if done is False:
                    try:
                        n_times = len(ds_times)
                    except:
                        n_times = 1
                    times.append(n_times)

            df["ntimes"] = times

            df = df.loc[
                :,
                [
                    "variable",
                    "ntimes",
                    "npoints",
                    "nlevels",
                    "long_name",
                    "unit",
                    "data_type",
                ],
            ]
            list_contents.append(df.assign(file=ff))

        if len(list_contents) == 1:
            return list_contents[0].drop(columns="file")

        if use_names == False:
            new_df = []
            i = 1
            for x in list_contents:
                new_df.append(x.assign(file=f"file {i}"))
                i += 1

            new_df = pd.concat(new_df)

            if len(set(new_df.file)) == 1:
                return new_df.drop(columns="file")
            else:
                new_df = new_df.set_index("file")
                return new_df
        else:
            return pd.concat(list_contents).set_index("file")

    @property
    def variables_detailed(self):
        """
        Detailed list of variables contained in a dataset.
        This will only display the variables in the first file of an ensemble.
        """

        if len(self) > 1:
            return (
                "This DataSet object is a mult-file dataset. Please inspect individual"
                "files using nc_variables"
            )

        cdo_result = subprocess.run(
            "cdo showname " + self.current[0],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        cdo_result = (
            str(cdo_result.stdout)
            .replace("b'", "")
            .replace("\\n", "")
            .replace("'", "")
            .strip()
        )
        cdo_result = cdo_result.split()
        dataset = Dataset(self.current[0])

        longs = None
        units = None
        longs = []
        for x in cdo_result:
            try:
                longs.append(dataset.variables[x].long_name)
            except:
                longs.append(None)
        # longs = [dataset.variables[x].long_name for x in cdo_result]
        units = []
        for x in cdo_result:
            try:
                units.append(dataset.variables[x].units)
            except:
                units.append(None)
        ##units = [dataset.variables[x].units for x in cdo_result]

        if longs is None and units is None:
            return cdo_result

        out = subprocess.run(
            "cdo sinfon " + self.current[0],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out = out.stdout.decode("utf-8")
        out = out.split("\n")
        out_inc = ["Grid coordinates :" in ff for ff in out]
        var_det = []
        i = 1
        while True:
            if out_inc[i]:
                break
            i += 1
            var_det.append(out[i - 1])

        var_det = [ff.replace(":", "") for ff in var_det]
        var_det = [" ".join(ff.split()) for ff in var_det]
        var_det = [
            ff.replace("Parameter name", "variable").split(" ") for ff in var_det
        ]
        df_vars = var_det[1:]
        labels = var_det[0]

        df = pd.DataFrame.from_records(df_vars, columns=labels)
        df = df.loc[:, ["Levels", "Points", "variable"]]
        df = df.rename(columns={"Levels": "levels", "Points": "points"})

        df = pd.DataFrame({"variable": cdo_result}).merge(df)

        if longs is not None:
            df["long_name"] = longs
        if units is not None:
            df["units"] = units

        df = df.assign(levels=lambda x: x.levels.astype("int")).assign(
            points=lambda x: x.points.astype("int")
        )

        return df

    @property
    def start(self):
        """
        The starting file or files of the DataSet object
        """
        return self._start

    @start.setter
    def start(self, value):
        if type(value) is str:
            self._start = [value]
        if isinstance(value, list):
            self._start = value

    @property
    def current(self):
        """
        The current file or files in the DataSet object
        """
        return self._current

    @current.setter
    def current(self, value):
        for ff in self:
            remove_safe(ff)

        if type(value) is str:
            append_safe(value)
            self._current = [value]
        if isinstance(value, list):
            self._current = value

            for ff in value:
                append_safe(ff)

    @property
    def history(self):
        """
        The history of operations on the DataSet
        """
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    def copy(self):
        """
        Make a deep copy of an DataSet object
        """
        self.run()

        new = copy.deepcopy(self)
        for ff in new:
            append_safe(ff)
        return new

    def __del__(self):
        for ff in self:
            remove_safe(ff)
        for ff in self._safe:
            remove_safe(ff)
        if self._weights is not None:
            remove_safe(self._weights)
        if self._weights is not None:
            remove_safe(self._grid)

        cleanup()

    @start.deleter
    def start(self):
        raise AttributeError("You cannot delete the start point")

    # import the methods

    from nctoolkit.add_etc import abs
    from nctoolkit.add_etc import add
    from nctoolkit.add_etc import exp
    from nctoolkit.add_etc import log
    from nctoolkit.add_etc import log10
    from nctoolkit.add_etc import subtract
    from nctoolkit.add_etc import multiply
    from nctoolkit.add_etc import divide
    from nctoolkit.add_etc import power
    from nctoolkit.add_etc import square
    from nctoolkit.add_etc import sqrt

    from nctoolkit.anomaly import annual_anomaly
    from nctoolkit.anomaly import monthly_anomaly

    from nctoolkit.append import append
    from nctoolkit.append import remove

    from nctoolkit.assign import assign

    from nctoolkit.cdo_command import cdo_command
    from nctoolkit.cellareas import cell_area

    from nctoolkit.centres import centre

    from nctoolkit.cleanup import disk_clean

    from nctoolkit.compare import compare

    from nctoolkit.compare_data import gt
    from nctoolkit.compare_data import lt

    from nctoolkit.corr import cor_space
    from nctoolkit.corr import cor_time

    from nctoolkit.crop import crop

    from nctoolkit.distgrid import distribute

    from nctoolkit.drop import drop

    from nctoolkit.ensembles import ensemble_mean
    from nctoolkit.ensembles import ensemble_max
    from nctoolkit.ensembles import ensemble_min
    from nctoolkit.ensembles import ensemble_range
    from nctoolkit.ensembles import ensemble_stdev
    from nctoolkit.ensembles import ensemble_sum
    from nctoolkit.ensembles import ensemble_var

    from nctoolkit.ensembles import ensemble_percentile

    from nctoolkit.esoteric import assign_coords
    from nctoolkit.esoteric import set_gridtype

    from nctoolkit.fill import fill_na

    from nctoolkit.fldstat import spatial_mean
    from nctoolkit.fldstat import spatial_min
    from nctoolkit.fldstat import spatial_max
    from nctoolkit.fldstat import spatial_range
    from nctoolkit.fldstat import spatial_sum
    from nctoolkit.fldstat import spatial_percentile

    from nctoolkit.fldstat import box_mean
    from nctoolkit.fldstat import box_max
    from nctoolkit.fldstat import box_min
    from nctoolkit.fldstat import box_sum
    from nctoolkit.fldstat import box_range

    from nctoolkit.format import format

    from nctoolkit.inttime import time_interp
    from nctoolkit.inttime import timestep_interp

    from nctoolkit.masking import mask_box

    from nctoolkit.mergers import collect
    from nctoolkit.mergers import merge

    from nctoolkit.meridonials import meridonial_mean
    from nctoolkit.meridonials import meridonial_min
    from nctoolkit.meridonials import meridonial_max
    from nctoolkit.meridonials import meridonial_range

    from nctoolkit.nco_command import nco_command

    from nctoolkit.phenology import phenology

    # from nctoolkit.phenology import initiation

    from nctoolkit.plot import plot

    from nctoolkit.reduce import reduce_dims

    from nctoolkit.reduce_grid import reduce_grid

    from nctoolkit.regrid import regrid

    from nctoolkit.rename import rename

    from nctoolkit.resample import resample_grid

    from nctoolkit.rollstat import rolling_mean
    from nctoolkit.rollstat import rolling_min
    from nctoolkit.rollstat import rolling_max
    from nctoolkit.rollstat import rolling_range
    from nctoolkit.rollstat import rolling_sum

    from nctoolkit.run import run

    from nctoolkit.select import select

    from nctoolkit.setters import set_date
    from nctoolkit.setters import set_missing
    from nctoolkit.setters import set_units
    from nctoolkit.setters import set_longnames
    from nctoolkit.setters import set_precision

    from nctoolkit.shift import shift

    from nctoolkit.split import split

    from nctoolkit.strip_vars import strip_variables
    from nctoolkit.sumall import sum_all

    from nctoolkit.temporal_stat import tmean
    from nctoolkit.temporal_stat import tpercentile
    from nctoolkit.temporal_stat import tmax
    from nctoolkit.temporal_stat import tmedian
    from nctoolkit.temporal_stat import tmin
    from nctoolkit.temporal_stat import trange
    from nctoolkit.temporal_stat import tvar
    from nctoolkit.temporal_stat import tvariance
    from nctoolkit.temporal_stat import tstdev
    from nctoolkit.temporal_stat import tsum
    from nctoolkit.temporal_stat import tcumsum
    from nctoolkit.temporal_stat import na_count
    from nctoolkit.temporal_stat import na_frac

    from nctoolkit.thresholds import first_above
    from nctoolkit.thresholds import first_below
    from nctoolkit.thresholds import last_above
    from nctoolkit.thresholds import last_below

    from nctoolkit.to_lonlat import to_latlon

    from nctoolkit.to_nc import to_nc

    from nctoolkit.toxarray import to_xarray
    from nctoolkit.toxarray import to_dataframe

    from nctoolkit.verticals import vertical_mean
    from nctoolkit.verticals import vertical_min
    from nctoolkit.verticals import vertical_max
    from nctoolkit.verticals import vertical_range
    from nctoolkit.verticals import vertical_sum
    from nctoolkit.verticals import vertical_integration
    from nctoolkit.verticals import vertical_cumsum
    from nctoolkit.verticals import top
    from nctoolkit.verticals import vertical_interp
    from nctoolkit.verticals import bottom
    from nctoolkit.verticals import bottom_mask
    from nctoolkit.verticals import invert_levels

    from nctoolkit.zip import zip

    from nctoolkit.zonals import zonal_mean
    from nctoolkit.zonals import zonal_min
    from nctoolkit.zonals import zonal_max
    from nctoolkit.zonals import zonal_range

    # Deprecated methods
    from nctoolkit.deprecated import merge_time
    from nctoolkit.deprecated import surface
