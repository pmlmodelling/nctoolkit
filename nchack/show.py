
import subprocess
import pandas as pd

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
    cdo_result = subprocess.run("cdo showname" + self.current, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result.sort()
    return cdo_result

def years(self):
    cdo_result = subprocess.run("cdo showyear" + self.current, shell = True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cdo_result = str(cdo_result.stdout).replace("\\n", "")
    cdo_result = cdo_result.replace("b'", "").strip()
    cdo_result = cdo_result.replace("'", "").strip()
    cdo_result = cdo_result.split()
    cdo_result = list(set(cdo_result))
    cdo_result =  [int(v) for v in cdo_result]
    cdo_result.sort()
    return cdo_result

def months(self):
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

    out = subprocess.run("cdo showatts " + self.current, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for ll in str(out.stdout).replace("b'", "").split("\\n"):
        print(ll)

def global_attributes(self):

    out = subprocess.run("cdo showattsglob " + self.current, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    for ll in str(out.stdout).replace("b'", "").split("\\n"):
        print(ll)



