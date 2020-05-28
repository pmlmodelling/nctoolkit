
import os
from nctoolkit.api import open_data
from nctoolkit.cleanup import cleanup, disk_clean
from nctoolkit.flatten import str_flatten
from nctoolkit.generate_grid import generate_grid
from nctoolkit.runthis import run_this
from nctoolkit.regrid import regrid
from nctoolkit.session import nc_safe
from nctoolkit.temp_file import temp_file


def to_latlon(self, lon=None, lat=None, res=None, method="bil"):
    """
    Regrid a dataset to a regular latlon grid

    Parameters
    -------------
    lon : list
        2 element list giving minimum and maximum longitude of target grid
    lat : list
        2 element list giving minimum and maximum latitude of target grid
    res : float, int or list
        If float or int given, this will be the horizontal and vertical resolution of the target grid.
        If 2 element list is given, the first element is the longitudinal resolution and the second is the latitudinal resolution.
    method : str
        remapping method. Defaults to "bil". Bilinear: "bil"; Nearest neighbour: "nn",....
    """

    if lon is None:
        raise ValueError("Please supply lon")
    if lat is None:
        raise ValueError("Please supply lat")
    if res is None:
        raise ValueError("Please supply res")

    if (type(lon) is not list) and (type(lat) is not list):
        raise TypeError("Check that lon/lat ranges are lists")

    if len(lon) != 2:
        raise ValueError("lon is a list of more than 2 variables")

    if len(lat) != 2:
        raise ValueError("lat is a list of more than 2 variables")

    for ll in lon:
        if (type(ll) is not int) and (type(ll) is not float):
            raise TypeError(f"{ll} from lon is not an int or float")

    for ll in lat:
        if (type(ll) is not int) and (type(ll) is not float):
            raise TypeError(f"{ll} from lat is not an int or float")

    # now, clip to the lonlat box we need

    if lat[1] < lat[0]:
        raise ValueError("Check lat order")
    if lon[1] < lon[0]:
        raise ValueError("Check lon order")

    if type(res) is int:
        res = float(res)

    if (type(res) is not float) and (type(res) is not list):
        raise TypeError("res supplied is not valid")

    if type(res) is float:
        res = [res, res]

    if type(res) is list:
        if type(res[0]) is int:
            res[0] = float(res[0])
        if type(res[1]) is int:
            res[1] = float(res[1])

        if (type(res[0]) is not float) or (type(res[1]) is not float):
            raise TypeError("res supplied is not valid")
        if (res[0] <= 0) or (res[1] <= 0):
            raise ValueError("Check res supplied are positive values")

    # create the grid and save it to temp

    grid_file = temp_file()[0:-2]

    xsize = int((lon[1] - lon[0]) / res[0]) + 1
    ysize = int((lat[1] - lat[0]) / res[1]) + 1
    lon_step = res[0]
    lat_step = res[1]
    f = open(grid_file, "w")
    f.write("gridtype = lonlat\n")
    f.write("xsize = " + str(xsize) + "\n")
    f.write("ysize = " + str(ysize) + "\n")
    f.write("xfirst = " + str(lon[0]) + "\n")
    f.write("yfirst = " + str(lat[0]) + "\n")
    f.write("xname = " + "lon" + "\n")
    f.write("xlongname = " + "Longitude" + "\n")
    f.write("xunits = " + "degrees_east" + "\n")
    f.write("yname = " + "lat" + "\n")
    f.write("ylongname = " + "Latitude" + "\n")
    f.write("yunits = " + "degrees_north" + "\n")

    f.write("xinc = " + str(lon_step) + "\n")
    f.write("yinc = " + str(lat_step) + "\n")
    f.close()

    nc_safe.append(grid_file)

    # call regrid
    self.regrid(grid=grid_file, method=method)

    nc_safe.remove(grid_file)

    #os.remove(grid_file)
    cleanup()
