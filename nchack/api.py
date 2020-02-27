# import packages
import os
import re
from netCDF4 import Dataset
import copy
import random
import string
import xarray as xr
import pandas as pd
import subprocess
import sys
import warnings
import atexit
import multiprocessing as mp


# A custom format for warnings.
def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

warnings.formatwarning = custom_formatwarning

# import functions from nchack
from .cleanup import cleanup
from .cleanup import clean_all
from .cleanup import deep_clean
from .cleanup import temp_check
from .create_ensemble import create_ensemble
from .flatten import str_flatten
from .generate_grid import generate_grid
from .runthis import run_cdo
from .session import nc_safe
from .session import nc_protected
from .session import session_info
from .show import nc_variables
from .show import nc_years
from .temp_file import temp_file

# set up the session info
letters = string.ascii_lowercase
session_info["stamp"] = "nchack" + "".join(random.choice(letters) for i in range(8)) + "nchack"
session_info["temp_dir"] = "/tmp/"
session_info["thread_safe"] = False
session_info["lazy"] = False
result = os.statvfs("/tmp/")
session_info["size"] = result.f_frsize * result.f_bavail
session_info["latest_size"] = 0
session_info["cores"] = 1

# register clean_all to clean temp files on exit
atexit.register(clean_all)

# run temp_check to see if any files are held over from previous sessions
temp_check()


def options(**kwargs):
    """
    Define session options.
    Set the options in the session. Available options are thread_safe and lazy.
    Set thread_safe = True if hdf5 was built to be thread safe.
    Set lazy = True if you want methods to evaluate lazy by default.

    Parameters
    ---------------
    **kwargs
        Define options using key, value pairs.

    """

    valid_keys = ["thread_safe", "lazy", "cores"]

    for key in kwargs:
        if key not in valid_keys:
            raise AttributeError(key + " is not a valid option")
        if type(kwargs[key]) is not bool:
            if key == "cores":
                if type(kwargs[key]) is int:
                    if kwargs[key] > mp.cpu_count():
                        raise ValueError(str(kwargs[key]) + " is greater than the number of system cores (" + str(mp.cpu_count()) + ")")
                    session_info[key] = kwargs[key]
                else:
                    raise TypeError("cores must be an int")
            else:
                raise AttributeError(key + " is not valid session info!")
        else:
            session_info[key] = kwargs[key]


def convert_bytes(num):
    """
     A function to make file size human readable
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
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



def open_data(x = None, suppress_messages = False, checks = False):
    """
    Read netcdf data as a DataSet object

    Parameters
    ---------------
    x : str or list
        A string or list of netcdf files. The function will check the files exist. If x is not a list, but an iterable it will be converted to a list
    checks: boolean
        Do you want basic checks to ensure cdo can read files?
    """

    # make sure data has been supplied
    if x is None:
            raise ValueError("No data was supplied!")

    # coerce an iterable to a list
    if type(x) is not str:
        x = [y for y in x]
        for ff in x:
            if type(ff) is not str:
                raise TypeError("You have not supplied an iterable made of file paths!")


    # check the files provided exist
    if type(x) is str:
        if os.path.exists(x) == False:
            raise ValueError("Data set " + x + " does not exist!")

        if checks:
            out = subprocess.run("cdo sinfo " + x, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            if "Open failed" in out.stderr.decode("utf-8"):
                mes = out.stderr.decode("utf-8").replace("cdo    sinfo: ", "").replace("<\n", "").replace("\n", "")
                mes = re.sub(" +", " ", mes)
                raise ValueError(mes)


        else:
            nc_safe.append(x)
            nc_protected.append(x)


    # it's possible there are duplicates in the data
    # Get rid of them..
    # Note: This will also ensure the original list is deep copied

    if type(x) is list:
        orig_size = len(x)
        x = list(dict.fromkeys(x))
        if len(x) < orig_size:
            warnings.warn(message = "Duplicates in data set have been removed!")

    if type(x) is list:
        if checks:
            if suppress_messages == False:
                if len(x) > 500:
                    print("Performing basic checks on ensemble files")
        if len(x) == 0:
            raise ValueError("You have not provided any files!")

        for ff in x:

            if os.path.exists(ff) == False:
                raise ValueError("Data set " + ff + " does not exist!")
            else:
                if checks:
                    out = subprocess.run("cdo sinfo " + ff, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                    if "Open failed" in out.stderr.decode("utf-8"):
                        mes = out.stderr.decode("utf-8").replace("cdo    sinfo: ", "").replace("<\n", "").replace("\n", "")
                        mes = re.sub(" +", " ", mes)
                        raise ValueError(mes)
                nc_safe.append(ff)
                nc_protected.append(x)
        if checks:
            if suppress_messages == False:
                if len(x) > 500:
                    print("All files passed checks")

    # if there is only one file in the list, change it to a single file
    if type(x) is list:
        if len(x) == 1:
            x = x[0]

    return DataSet(x)


def merge(*datasets, match = ["day", "year", "month"]):
    all_files = []
    for dataset in datasets:
        if "DataSet" in str(type(dataset)) == False:
            raise ValueError("Please check everything is an DataSet object!")
        # make sure everything has been evaluated
        dataset.release()
        if type(dataset.current) is str:
            all_files += [dataset.current]
        else:
            all_files += dataset.current
    result = open_data(all_files)
    result.merge(match = match)
    return result

def cor_time(x = None, y = None):

    if "DataSet" in str(type(x)) == False:
        raise ValueError("Please check x is a dataset")
        # make sure everything has been evaluated
        x.release()

    if "DataSet" in str(type(y)) == False:
        raise ValueError("Please check y is a dataset")
        # make sure everything has been evaluated
        y.release()

    if type(x.current) is not str or type(y.current) is not str:
        raise TypeError("This method can only work for single variable data sets")

    target = temp_file("nc")
    command = "cdo -L timcor " + x.current + " " + y.current + " " + target
    target = run_cdo(command, target = target)

    data = open_data(target)

    return data






class DataSet(object):
    """
    A modifiable ensemble of netcdf files
    """
    def __init__(self, start = ""):
        """Initialize the starting file name etc"""
        # Attribuates of interest to users
        self.history = []
        self.start = start
        self.current = start

        # attributes to the module, but not users (probably)
        self._weights = None
        if session_info["lazy"]:
            self._run = False
        else:
            self._run = True
        self._hold_history = []
        self._merged = False


    def __getitem__(self, index):
        if type(self.current) is str:
            return self.current

        return self.current[index]

    def __len__(self):
        if type(self.current) is str:
            return 1

        return len(self.current)

    def __iter__(self):
        if type(self.current) is str:
            yield self.current
            return
        if type(self.current) is list:
            for ff in self.current:
                yield ff
            return

    def __repr__(self):
        # tidy up the output first
        if isinstance(self.start,list):
            if len(self.start) > 10:
                start = ">10 ensemble member"
                start = str(len(self.start)) + " member ensemble"
            else:
                start = str_flatten(self.start)
        if type(self.start) == str:
            start = self.start

        if isinstance(self.current,list):
            if len(self.current) > 10:
                current = str(len(self.current)) + " member ensemble"
            else:
                current = str_flatten(self.current)
        if type(self.current) == str:
            current = self.current

        return "<nchack.DataSet>:\nstart: " + start + "\ncurrent: " + current + "\noperations: " + str(len(self.history))


    @property
    def size(self):
        """The size of an object
        This will print the number of files, total size, and smallest and largest files in an DataSet object.
        """
        if type(self.current) is str:
            result = "Number of files: 1\n"
            result = result + "File size: " + convert_bytes(file_size(self.current))
            print(result)
        else:
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
            result = "Number of files in ensemble: " + str(len(self.current)) + "\n"
            result = result + "Ensemble size: " + sum_size  + "\n"
            result = result + "Smallest file: " + smallest_file + " has size "  + min_size  + "\n"
            result = result + "Largest file: " + largest_file + " has size "  + max_size
            print(result)

    @property
    def variables(self):
        """
        Variables contained in an object's netcdf file.
        This will check the netcfile's contents, if it is a single file DataSet object.
        """

        if type(self.current) is list:
            raise TypeError("This DataSet object is a list. Please inspect individual files using nc_variables")

        cdo_result = subprocess.run("cdo showname " + self.current, shell = True, stdout=subprocess.PIPE , stderr=subprocess.PIPE  )
        cdo_result = str(cdo_result.stdout).replace("b'", "").replace("\\n", "").replace("'", "").strip()
        cdo_result = cdo_result.split()

        return(cdo_result)

    @property
    def variables_detailed(self):
        """
        Variables contained in an object's netcdf file.
        This will check the netcfile's contents, if it is a single file DataSet object.
        """

        if type(self.current) is list:
            print("This DataSet object is a list. Please inspect individual files using nc_variables")

        cdo_result = subprocess.run("cdo showname " + self.current, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cdo_result = str(cdo_result.stdout).replace("b'", "").replace("\\n", "").replace("'", "").strip()
        cdo_result = cdo_result.split()
        dataset = Dataset(self.current)

        longs = None
        units = None
        if "long_name" in str(dataset.variables[cdo_result[0]]):
                longs = [dataset.variables[x].long_name for x in cdo_result]
        if "units" in str(dataset.variables[cdo_result[0]]):
                units = [dataset.variables[x].units for x in cdo_result]

        if longs is None and units is None:
            return(cdo_result)

        out = subprocess.run("cdo sinfon " + self.current, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = out.stdout.decode('utf-8')
        out = out.split("\n")
        out_inc = ["Grid coordinates :" in ff for ff in out]
        var_det = []
        i = 1
        while True:
            if out_inc[i]:
                break
            i+=1
            var_det.append(out[i-1])

        var_det = [ff.replace(":", "") for ff in var_det]
        var_det = [" ".join(ff.split()) for ff in var_det]
        var_det = [ff.replace("Parameter name", "variable").split(" ") for ff in var_det]
        sales = var_det[1:]
        labels = var_det[0]
        df = pd.DataFrame.from_records(sales, columns=labels)
        df = df.loc[:, ["Levels", "Points", "variable"]]
        df = df.rename(columns = {"Levels":"levels", "Points":"points"})

        df = pd.DataFrame({"variable": cdo_result}).merge(df)

        if longs is not None:
            df["long_name"] = longs
        if units is not None:
            df["units"] = units

        df = (
                df
                .assign(levels = lambda x: x.levels.astype("int"))
                .assign(points = lambda x: x.points.astype("int"))
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
            self._start = value
        if isinstance(value,list):
            self._start = value

    @property
    def current(self):
        """
        The current file or files in the DataSet object
        """
        return self._current

    @current.setter
    def current(self, value):
        if type(value) is str:
            self._current = value
        if isinstance(value,list):
            if len(value) > 1:
                self._current = value
            else:
                self._current = value[0]


    @property
    def history(self):
        """
        The history of operations on the DataSet
        """
        return self._history

    @history.setter
    def history(self, value):
        self._history = value

    @property
    def run(self):
        """
        Is the object in run or lazy eval mode?
        """
        return self._run

    @run.setter
    def run(self, value):
        self._run = value


    def copy(self):
        """
        Make a deep copy of an DataSet object
        """
        self.release()

        new = copy.deepcopy(self)
        if type(new.current) is str:
            nc_safe.append(new.current)
        else:
            for ff in new:
                nc_safe.append(ff)
        return new

    def __del__(self):
        if type(self.current) is str:
            if self.current in nc_safe:
                nc_safe.remove(self.current)
            if self._weights in nc_safe:
                nc_safe.remove(self._weights)
        else:
            for ff in self:
                if ff in nc_safe:
                    nc_safe.remove(ff)

        cleanup()

    @start.deleter
    def start(self):
        raise AttributeError("You cannot delete the start point")

    from .toxarray import to_xarray
    from .toxarray import to_dataframe

    from .cellareas import cell_areas
    from .regrid import regrid

    from .ensembles import ensemble_mean
    from .ensembles import ensemble_max
    from .ensembles import ensemble_min
    from .ensembles import ensemble_range
    from .ensembles import ensemble_percentile

    from .clip import clip
    from .select import select_variables
    from .select import select_timestep

    from .cdo_command import cdo_command
    from .nco_command import nco_command

    from .expr import mutate
    from .expr import transmute
    from .expr import sum_all

    from .select import select_season
    from .select import select_months
    from .select import select_years

    from .seasstat import seasonal_mean
    from .seasstat import seasonal_min
    from .seasstat import seasonal_max
    from .seasstat import seasonal_range

    from .seasclim import seasonal_mean_climatology
    from .seasclim import seasonal_min_climatology
    from .seasclim import seasonal_max_climatology
    from .seasclim import seasonal_range_climatology

    from .yearlystat import annual_mean
    from .yearlystat import annual_min
    from .yearlystat import annual_max
    from .yearlystat import annual_range

    from .monstat import monthly_mean
    from .monstat import monthly_min
    from .monstat import monthly_max
    from .monstat import monthly_range

    from .monthlyclim import monthly_mean_climatology
    from .monthlyclim import monthly_min_climatology
    from .monthlyclim import monthly_max_climatology
    from .monthlyclim import monthly_range_climatology

    from .dailyclim import daily_mean_climatology
    from .dailyclim import daily_min_climatology
    from .dailyclim import daily_max_climatology
    from .dailyclim import daily_range_climatology

    from .to_nc import write_nc

    from .rename import rename

    from .setters import set_date
    from .setters import set_missing
    from .setters import set_units
    from .setters import set_longnames


    from .esoteric import set_attributes
    from .esoteric import delete_attributes

    from .esoteric import assign_coords
    from .esoteric import set_gridtype




    from .time_stat import mean
    from .time_stat import percentile
    from .time_stat import max
    from .time_stat import min
    from .time_stat import range
    from .time_stat import var
    from .time_stat import sum
    from .time_stat import cum_sum

    from .release import release

    from .delete import remove_variables

    from .mergers import merge_time
    from .mergers import merge

    from .rollstat import rolling_mean
    from .rollstat import rolling_min
    from .rollstat import rolling_max
    from .rollstat import rolling_range
    from .rollstat import rolling_sum

    from .show import times
    from .show import years
    from .show import months
    from .show import levels
    from .show import attributes
    from .show import global_attributes

    from .fldstat import spatial_mean
    from .fldstat import spatial_min
    from .fldstat import spatial_max
    from .fldstat import spatial_range
    from .fldstat import spatial_sum
    from .fldstat import spatial_percentile

    from .verticals import vertical_mean
    from .verticals import vertical_min
    from .verticals import vertical_max
    from .verticals import vertical_range
    from .verticals import vertical_sum
    from .verticals import vertical_cum
    from .verticals import surface
    from .verticals import vertical_interp
    from .verticals import bottom

    from .view import view

    from .zip import zip

    from .checkers import check_dates
    from .checkers import ensemble_check

    from .corr import cor_space
    from .corr import cor_time

    from .phenology import phenology

    from .split import split

    from .anomaly import annual_anomaly
    from .anomaly import monthly_anomaly

    from .masking import mask_box

    from .inttime import time_interp

    from .cleanup import disk_clean

    from .plot import plot


    from .compare import compare_all

    from .add_etc import add
    from .add_etc import subtract
    from .add_etc import multiply
    from .add_etc import divide
    from .cf_checks import cf_checks

    from .to_lonlat import to_lonlat

    from .reduce import reduce_dims



