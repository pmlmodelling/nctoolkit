import re
import subprocess

def name_check(x):

    if len(x) == 0:
        return False

    if " " in x:
        return False

    text = re.compile(".*[+,/,-,*]")
    if len(text.findall(x)) > 0:
        raise ValueError("Do not include mathematical operators in variable names")

    if len(x) == 1:
        text = re.compile("[a-zA-Z]")
        if text.match(x):
            return True
        else:
            return False
    text = re.compile("([a-zA-Z0-9_]|{MUTF8})([^\x00-\x1F/\x7F-\xFF]|{MUTF8})")
    # regex taken from https://www.unidata.ucar.edu/support/help/MailArchives/netcdf/msg10684.html

    if text.match(x):
        return True
    else:
        return False



def is_curvilinear(ff):
    """
    Function to work out if a file contains a curvilinear grid
    """
    cdo_result = subprocess.run(
        f"cdo sinfo {ff}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    return (
        len(
            [
                x
                for x in cdo_result.stdout.decode("utf-8").split("\n")
                if "curvilinear" in x
            ]
        )
        > 0
    )


def version_below(x, y):
    x = x.split(".")
    x = int(x[0]) * 1000 + int(x[1]) * 100 + int(x[2])

    y = y.split(".")
    y = int(y[0]) * 1000 + int(y[1]) * 100 + int(y[2])

    return x < y


def version_above(x, y):
    x = x.split(".")
    x = int(x[0]) * 1000 + int(x[1]) * 100 + int(x[2])

    y = y.split(".")
    y = int(y[0]) * 1000 + int(y[1]) * 100 + int(y[2])

    return x > y


# check version of cdo installed

def latest_version():
    try:
        import requests
    
        url = "https://anaconda.org/conda-forge/cdo"
        r = requests.get(url)
        import re
        text = re.compile("v.*..*..[0-10]")
    
        text = re.compile("v[0-9].[0-9]?[0-9].[0-9]?[0-9]")
        options = []
        for x in [text.findall(x) for x in r.text.split(" ") if "2.0.5" in x]:
            options += x
    
        versions = []
        for x in options:
            versions.append(x.replace("v", ""))
        versions = list(set(versions))
        if  len(versions) == 1:
            return versions[0]
        else:
            return None
    except:
        return None

def validate_version():
    """
    Function to tell the user whether a valid version of CDO is installed
    """
    bad = False

    try:
        version = cdo_version()
        bad = version_above(cdo_version(), "2.0.0") and version_below(cdo_version(), "2.0.5")
        actual_version = version
        if version is None:
            print(
                "Please install CDO version 1.9.7 or above: https://code.mpimet.mpg.de/projects/cdo/ or https://anaconda.org/conda-forge/cdo"
            )
        sub = "."
        wanted = ""
        n = 3
        where = [m.start() for m in re.finditer(sub, version)][n - 1]

        version = re.sub("[A-Za-z]", "", version)

        before = version[:where]
        after = version[where:]
        after = after.replace(sub, wanted)
        if version_below(cdo_version(), "1.9.7"):
            print(
                "Please install CDO version 1.9.7 or above: https://code.mpimet.mpg.de/projects/cdo/ or https://anaconda.org/conda-forge/cdo"
            )
        else:
            latest = latest_version()

            if latest is None:
                print(f"nctoolkit is using Climate Data Operators version {actual_version}")
            else:
                if version_below(actual_version, latest):
                    print(f"nctoolkit is using Climate Data Operators version {actual_version}. v{latest} is available: https://anaconda.org/conda-forge/cdo!")
                else:
                    print(f"nctoolkit is using the latest version of Climate Data Operators version: {actual_version}")


    except:
        print(
            "Please install CDO version 1.9.7 or above: https://code.mpimet.mpg.de/projects/cdo/ or https://anaconda.org/conda-forge/cdo"
        )
    if bad:
        raise ValueError(
            "This version of nctoolkit is not compatible with CDO versions 2.0.0 and above"
        )


def cdo_version():
    """
    Function to identify the CDO version
    """
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    version = [
        x for x in str(cdo_check.stderr).split("\n") if "version" in x and "cdo" in x
    ]
    if len(version) == 0:
        version = [
            x
            for x in str(cdo_check.stdout).split("\n")
            if "version" in x and "cdo" in x
        ]
        if len(version) == 0:
            return None
    version = version[0]

    candidates = [
        x for x in version.split(" ") if x.startswith("1") or x.startswith("2")
    ]
    return candidates[0]
