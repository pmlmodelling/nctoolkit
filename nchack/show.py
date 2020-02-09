
import subprocess
import pandas as pd
import numpy as np

def times(self):
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")

    cdo_result = subprocess.run("cdo showtimestamp " + self.current, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = pd.Series( (v for v in cdo_result) )

    return cdo_result

def levels(self):
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")
    """
    Method to get the depths available in a netcdf file
    """
    cdo_result = subprocess.run("cdo showlevel " + self.current, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result =  [float(v) for v in cdo_result]
    cdo_result.sort()
    return cdo_result


def nc_variables(ff):
    cdo_result = subprocess.run("cdo showname " + ff, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result.sort()
    return cdo_result

def years(self):
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")
    cdo_result = subprocess.run("cdo showyear " + self.current, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result =  [int(v) for v in cdo_result]
    cdo_result.sort()
    return cdo_result

def months(self):
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")
    cdo_result = subprocess.run("cdo showmon " + self.current, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result =  [int(v) for v in cdo_result]
    cdo_result.sort()
    return cdo_result



def attributes(self):
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")

    out = subprocess.run("cdo showatts " + self.current, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = out.stdout.decode('utf-8')
    return out

def global_attributes(self):
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")

    out = subprocess.run("cdo showattsglob " + self.current, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    out = out.stdout.decode('utf-8')
    return out



def cf_checks(self, version = None):
    """
    Method to run the cf checker from the Met Office on files
    """
    self.release()
    if type(self.current) is list:
        raise TypeError("This presently only works for single file datasets")

    if version is None:
        version = 1.6
        print("Using CF version 1.6")

    if version not in np.arange(1.0, 1.8, 0.1):
        raise ValueError("Version supplied is not valid!")

    version = str(version)
    command = "cfchecks " + "-v "  + version + " " + self.current
    out = subprocess.Popen(command,shell = True, stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    result,ignore = out.communicate()
    print(result.decode())


