
import glob
import os
import copy 
import pandas as pd

# function to find files in directory with a specified variable 

def create_ensemble(path = "", var = None, recursive = True):
    "A function to create an ensemble is valid"

    def intersection(lst1, lst2): 
        lst3 = [value for value in lst1 if value in lst2] 
        return lst3 
    # make sure the path exists

    if os.path.exists(path) == False:
        raise ValueError("The path provided does not exist!")
# check that the remapping method is valid

    # make sure the path ends with "/" if it is not empty

    if path != "":
        if path.endswith("/") == False:
            path = path + "/"


    if recursive:   
        files = [f for f in glob.glob(path + "**/*.nc", recursive=True)]
    else:
        files = [f for f in glob.glob(path + "*.nc", recursive=True)]
    
    if var is None:
        ensemble = copy.deepcopy(files)
    else: 
        ensemble = []
        for ff in files:
            cdo_result = os.popen( "cdo showname " + ff).read()
            cdo_result = cdo_result.replace("\n", "").strip().split(" ")
            if var in cdo_result:
                ensemble.append(ff)

    return ensemble

def generate_ensemble(path = "", recursive = True):
    "A function to create an ensemble is valid"
    ensemble = create_ensemble(path, recursive = recursive)
    all_info = []
    for ff in ensemble:
        cdo_info = os.popen( "cdo sinfon " + ff).read()
        cdo_times = os.popen( "cdo ntime " + ff).read() 
        cdo_times = cdo_times.replace("\n", "")
        cdo_times = int(cdo_times) 
        if cdo_times == 1:
            cdo_times = 1
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
        i_variables = os.popen( "cdo showname " + ff).read() 
        i_variables = i_variables.replace("\n", "").strip().split(" ")
        
        i_levels = os.popen( "cdo nlevel " + ff).read() 
        i_levels = i_levels.split("\n")
        i_levels = int(i_levels[0])
        
        i_dict = {"path": i_files, "variables":i_variables, "n_files": len(i_files),  "n_levels": i_levels}
        all_ensembles.append(i_dict)

    return all_ensembles
