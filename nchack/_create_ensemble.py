
import glob
import os
import copy 

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



