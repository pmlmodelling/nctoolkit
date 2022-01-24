import xarray as xr
from nctoolkit.runthis import run_this
from nctoolkit.utils import is_curvilinear
import subprocess


def check(self):
    """
    Check contents of files for common data problems.
    """

    print("*****************************************")
    print("Checking data types")
    print("*****************************************")
    self_contents = self.contents
    list1 = self_contents.reset_index(drop=True).data_type
    positions = [ind for ind, x in enumerate(list1) if x.startswith("I")]
    if len(positions):
        bad = list(self_contents.reset_index(drop=True).data_type[positions])

    if len(positions) > 0:
        check = ",".join(bad)
        if "," in check:
            print(
                f"The variable(s) {check} have integer data type. Consider setting data type to float 'F64' or 'F32' using set_precision."
            )
        else:
            print(
                f"The variable {check} has integer data type. Consider setting data type to float 'F64' or 'F32' using set_precision."
            )
    else:
        print("Variable checks passed")

    print("*****************************************")
    print("Running CF-compliance checks")
    print("*****************************************")

    cf_checker = True
    try:
        import cfchecker
    except:
        cf_checker = False
        print(
            "cfchecker is not available. Run 'pip install cfchecker' to check files for CF-compliance!"
        )

    if cf_checker:
        for ff in self:
            ds = xr.open_dataset(ff, decode_times=False)
            if "Conventions" not in list(ds.attrs.keys()):
                print(f"No CF-conventions in {ff}")
            else:
                version = ds.attrs["Conventions"].split("-")[1]

                command = f"cfchecks -v {version} {ff}"
                out = subprocess.Popen(
                    command,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                result, ignore = out.communicate()
                print(result.decode())
