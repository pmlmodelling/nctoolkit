
import glob
import os
import copy
import pandas as pd

# function to find files in directory with a specified variable

def create_ensemble(path = "", var = None, recursive = True):
    """
    Generate an ensemble

    Parameters
    -------------
    path: str
        The system to search for netcdf files
    var: str
        The variable the ensemble files must contain. This is ignored if not set.
    recursive : boolean
        True/False depending on whether you want to search the path recursively. Defaults to True.

    Returns
    -------------
    list
        A list of files
    """


    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3
    # make sure the path exists

    if os.path.exists(path) == False:
        raise ValueError("The path provided does not exist!")

    # make sure the path ends with "/" if it is not empty
    if path != "":
        if path.endswith("/") == False:
            path = path + "/"

    if recursive:
        files = [f for f in glob.glob(path + "/**/*.nc", recursive=True)]
    else:
        files = [f for f in glob.glob(path + "*.nc")]

    if var is None:
        ensemble = copy.deepcopy(files)
    else:
        ensemble = []
        for ff in files:
            cdo_result = os.popen(f"cdo showname {ff}").read()
            cdo_result = cdo_result.replace("\n", "").strip().split(" ")
            if var in cdo_result:
                ensemble.append(ff)

    return ensemble

def generate_ensemble(path = "", recursive = True):

    """
    A candidate ensemble generator. Ensembles are generated based on the distinct variable, time and grids available in the files detected in the given path.

    Parameters
    -------------
    path: str
        The system to search for netcdf files
    recursive : boolean
        True/False depending on whether you want to search the path recursively. Defaults to True.

    Returns
    -------------
    list
        A list of potential ensembles.
    """

    ensemble = create_ensemble(path, recursive = recursive)
    all_info = []
    for ff in ensemble:
        cdo_info = os.popen(f"cdo sinfon {ff}").read()
        cdo_times = os.popen(f"cdo ntime {ff}").read()
        cdo_times = cdo_times.replace("\n", "")
        cdo_times = int(cdo_times)
        # splitting by times is a bit tricky
        # Need to assume that files are roughly of the same time split. Example: you don't get one file with 1 year of data, but another with 20 years
        # Case 1: only one time step
        if cdo_times == 1:
            cdo_times = 1
        # Case 2: 2-7 time steps. This is probably only ever datasets with weekly data
        if cdo_times > 1 and cdo_times < 8:
            cdo_times = 2
        if cdo_times > 12:
            cdo_times = 3

        cdo_info = cdo_info[0:cdo_info.find("Time coord")]
        df = pd.DataFrame({"path":[ff], "info":[cdo_info], "times": [cdo_times]} )
        all_info.append(df)
    all_info = pd.concat(all_info)
    unique_info = all_info.drop(columns = ["path"]).drop_duplicates()

    all_ensembles = []

    for i in range(0, len(unique_info)):
        i_files = all_info.merge(unique_info.iloc[i:i+1,:]).path.tolist()
        ff = i_files[0]
        i_variables = os.popen(f"cdo showname {ff}").read()
        i_variables = i_variables.replace("\n", "").strip().split(" ")

        i_levels = os.popen(f"cdo nlevel {ff}").read()
        i_levels = i_levels.split("\n")
        i_levels = int(i_levels[0])

        i_dict = {"path": i_files, "variables":i_variables, "n_files": len(i_files),  "n_levels": i_levels}
        all_ensembles.append(i_dict)

    return all_ensembles
