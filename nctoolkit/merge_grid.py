
from nctoolkit.runthis import run_this
from nctoolkit.session import session_info

import warnings
import subprocess
from nctoolkit.flatten import str_flatten
from nctoolkit.temp_file import temp_file

def collect_grids(self):
    """
    Merge data with distinct grids
    These must be neighbouring latlon grids
    """

    self.run()

    n = len(self)
    cdo_command = f"cdo -collgrid,{n}"

    run_this(cdo_command, self, output="one")

    if session_info["lazy"]:
        self._merged = True

    return None

    if len(self) != 2:
        raise ValueError("merge_grids only works on 2 file datasets!")


    # extract the two grids

    ff = self[0]

    out1 = subprocess.run(

                 f"cdo griddes {ff}",
                 shell=True,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE,
             )

    out1 = out1.stdout.decode("utf-8")

    ff = self[1]
    out2 = subprocess.run(
                 f"cdo griddes {ff}",
                 shell=True,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE,
             )

    out2 = out2.stdout.decode("utf-8")

    grid1 = out1.split("\n")
    grid2 = out2.split("\n")

    if len([x for x in grid1 if "gridID" in x]) > 1:
        raise ValueError("You are trying to merge datasets with multiple grids!")

    if len([x for x in grid2 if "gridID" in x]) > 1:
        raise ValueError("You are trying to merge datasets with multiple grids!")


    if [x.split(" ")[-1] for x in grid1 if "gridtype" in x][0] != "lonlat":
        raise ValueError("The grids are not lonlat")

    if [x.split(" ")[-1] for x in grid2 if "gridtype" in x][0] != "lonlat":
        raise ValueError("The grids are not lonlat")

    # new size is the sum of the two sizes
    size_1 = int([x.split(" ")[-1] for x in grid1 if "gridsize" in x][0])

    size_2 = int([x.split(" ")[-1] for x in grid2 if "gridsize" in x][0])

    new_size = size_1 + size_2

    if [x.split(" ")[-1] for x in grid1 if "xinc" in x][0] != [x.split(" ")[-1] for x in grid2 if "xinc" in x][0]:
        raise ValueError("The xinc of the two files are different")

    if [x.split(" ")[-1] for x in grid1 if "yinc" in x][0] != [x.split(" ")[-1] for x in grid2 if "yinc" in x][0]:
        raise ValueError("The yinc of the two files are different")

    print(grid1)


    x_diff = [x.split(" ")[-1] for x in grid1 if "xfirst" in x][0] == [x.split(" ")[-1] for x in grid2 if "xfirst" in x][0]

    y_diff = [x.split(" ")[-1] for x in grid1 if "yfirst" in x][0] == [x.split(" ")[-1] for x in grid2 if "yfirst" in x][0]

    if x_diff and y_diff:
        raise ValueError("You are trying to merge datasets with the same xstart and ystart")


    # if the xstarts differ, we need to change the gridesize and xsize
    if x_diff is False:
        grid_file = temp_file()
        f = open(grid_file, "w")
        if float([x.split(" ")[-1] for x in grid1 if "xfirst" in x][0]) < float([x.split(" ")[-1] for x in grid2 if "xfirst" in x][0]):
            out_grid = grid1
        else:
            out_grid = grid2

        for l in out_grid:

            out_l = l

            if "gridsize" in l:
                out_l = f"gridsize  = {new_size}"

            if "xsize" in l:
                new_size = int([x.split(" ")[-1] for x in grid1 if "xsize" in x][0]) + int([x.split(" ")[-1] for x in grid2 if "xsize" in x][0])
                out_l = f"xsize     = {new_size}"


            print(out_l)
            f.write(f"{out_l}\n")





    #if y_diff is False:
    #    if float([x.split(" ")[-1] for x in grid1 if "yfirst" in x][0]) < float([x.split(" ")[-1] for x in grid2 if "yfirst" in x][0]):
    #        out_grid = grid1
    #    else:
    #        out_grid = grid2

    #    for l in out_grid:

    #        out_l = l

    #        if "gridsize" in l:
    #            out_l = f"gridsize  = {new_size}"

    #        if "ysize" in l:
    #            new_size = int([x.split(" ")[-1] for x in grid1 if "ysize" in x][0]) + int([x.split(" ")[-1] for x in grid2 if "ysize" in x][0])
    #            out_l = f"ysize     = {new_size}"


    #        print(out_l)

    #        grid_file = temp_file()





   # cdo_command = "cdo -mergegrid"

   # run_this(cdo_command, self, output="one")

   # if session_info["lazy"]:
   #     self._merged = True



