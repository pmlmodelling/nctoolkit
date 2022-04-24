import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"



class TestPercentile:
    def test_crop(self):

        byes = []
        byes.append("time")
        byes.append(["month", "year"])
        byes.append(["day", "year"])
        byes.append(["day"])
        byes.append(["year"])
        byes.append(["month"])
        byes.append(["season"])
        byes.append(["season", "year"])

        for by in byes:

            data = nc.open_data(ff)

            data.tpercentile(p = 50, over = by)
            print(data.history)
            commands = data.history[0].split(" ")

            data = nc.open_data(ff)
            data.tmin(over = by)
            part1 = data.history[0].split(" ")[-1]

            data = nc.open_data(ff)
            data.tmax(over = by)
            part2 = data.history[0].split(" ")[-1]

            assert commands[4] == part1

            assert commands[6] == part2
            part0 = part1.replace("min","pctl")
            pct_c = [x for x in commands if "pct" in x][0].split(",")[0]
            assert pct_c == part0



