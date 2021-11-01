import nctoolkit as nc
import subprocess
import platform
import pandas as pd
import xarray as xr
import os, pytest
import random
import numpy as np

nc.options(lazy=True)


ff = "data/sst.mon.mean.nc"


class TestAssign:
    import pandas as pd
    import numpy as np

    def test_assign(self):
        with pytest.raises(TypeError):
            nc.temp_file.temp_file(1)

    ds = nc.open_data("data/woa18_decav_t01_01.nc")
    with pytest.raises(ValueError):
        ds.assign(t_an = lambda x: x.t_an == vert_max(x.t_an), drop = True)
    with pytest.raises(ValueError):
        ds.assign(t_an = lambda x: x.t_an == spati_max(x.t_an), drop = True)
    with pytest.raises(ValueError):
        ds.assign(t_an = lambda x: x.t_an == zon_max(x.t_an), drop = True);ds.assign(t_an = lambda x: x.tan - 8)
    with pytest.raises(ValueError):
        ds.assign(t_an = lambda x: x.t_an == zon_max(x.t_an), drop = True);ds.assign(t_an = lambda x: x.tan - 8)
    with pytest.raises(ValueError):
        ds.assign(
            t_an = lambda x: x.t_an == zon_max(x.t_an), drop = True)
    with pytest.raises(ValueError):
        this = "x"
        ds.assign(
            t_an = lambda x: x.t_an + this, drop = True)

    ds.assign(t_an = lambda x: x.t_an == vertical_max(x.t_an), drop = True)
    ds.vertical_max()
    ds.spatial_max()
    assert ds.to_dataframe().t_an.values[0] == 1.0

    ds = nc.open_data("data/woa18_decav_t01_01.nc")
    ds.assign(t_an = lambda x: x.t_an is False) 
    assert ds.history[0] == "cdo -aexpr,'t_an=t_an<1'"

    ds = nc.open_data("data/woa18_decav_t01_01.nc")
    ds.assign(t_an = lambda x: x.t_an is True) 
    assert ds.history[0] == "cdo -aexpr,'t_an=t_an>0'"

    ds = nc.open_data("data/woa18_decav_t01_01.nc")
    ds.assign(t_an = lambda x: x.t_an == True) 
    assert ds.history[0] == "cdo -aexpr,'t_an=t_an>0'"

    ds = nc.open_data("data/woa18_decav_t01_01.nc")
    ds.assign(t_an = lambda x: x.t_an == False) 
    assert ds.history[0] == "cdo -aexpr,'t_an=t_an<1'"

    ff = "data/sst.mon.mean.nc"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + 273.15)
    print(data.history)
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + 273.15, drop=True)
    assert data.history[0] == "cdo -expr,'new=sst+273.15'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + [273.15][0])
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    k = [273.15]
    data.assign(new=lambda x: x.sst + k[0])
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    k = [273.15]
    data.assign(new=lambda x: x.sst + k[0])
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    k = 273.15
    data.assign(new=lambda x: x.sst + k)
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    k = 273.15
    data.assign(new=lambda x: x.sst + pd.DataFrame({"x": [273.15]}).x[0])
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    k = 273.15

    class MyClass:
        t = 273.15


    k = MyClass()
    data.assign(new=lambda x: x.sst + k.t)
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    k = 273.15
    data.assign(new=lambda x: x.sst + np.mean(k))
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    k = [273.15]
    data.assign(new=lambda x: x.sst + np.mean(k))
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    k = [273.15, 273.15]
    data.assign(new=lambda x: x.sst + np.mean(k))
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    k = [273.15, 273.15]
    data.assign(new=lambda x: x.sst + np.mean([273.15]))
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst ** 2)
    assert data.history[0] == "cdo -aexpr,'new=sst^2'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst > 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst>2)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst < 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst<2)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst <= 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst<=2)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst >= 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst>=2)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst == 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst==2)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst > 2) | (x.sst < 10))
    assert data.history[0] == "cdo -aexpr,'new=(sst>2)||(sst<10)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst == 2) | (x.sst < 10))
    assert data.history[0] == "cdo -aexpr,'new=(sst==2)||(sst<10)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst != 2) | (x.sst < 10))
    assert data.history[0] == "cdo -aexpr,'new=(sst!=2)||(sst<10)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst != 2) & (x.sst < 10))
    assert data.history[0] == "cdo -aexpr,'new=(sst!=2)&&(sst<10)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: sqrt(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: sqrt(x.sst + 2))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst+2)'"

    data = nc.open_data(ff)
    k = 2
    data.assign(new=lambda x: sqrt(x.sst + k))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst+2)'"

    data = nc.open_data(ff)
    k = [2, 1]
    data.assign(new=lambda x: sqrt(x.sst + k[0]))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst+2)'"

    data = nc.open_data(ff)
    k = [2, 1, [2]]
    data.assign(new=lambda x: sqrt(x.sst + k[2][0]))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst+2)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst+sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst - x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst-sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst*sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst / x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst/sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst ** x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst^sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: (x.sst + x.sst))
    assert data.history[0] == "cdo -aexpr,'new=(sst+sst)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: ((x.sst + x.sst) + np.mean(2)))
    assert data.history[0] == "cdo -aexpr,'new=((sst+sst)+2.0)'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + np.mean(2) + np.mean(2) + np.mean(2))
    assert data.history[0] == "cdo -aexpr,'new=sst+2.0+2.0+2.0'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + np.mean(2) + np.mean(2) + np.mean(2) - x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst+2.0+2.0+2.0-sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + np.mean(np.mean(2)) + np.mean(2) + np.mean(2) - x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst+2.0+2.0+2.0-sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + 273.15, old=lambda x: x.sst)
    data.history[0] == "cdo -aexpr,'new=sst+273.15;old=sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + 273.15,
            old=lambda x: x.sst)
    data.history[0] == "cdo -aexpr,'new=sst+273.15;old=sst'"


    data = nc.open_data(ff)
    data.assign(new = lambda x:
            x.sst + 273.15,
            old=lambda
            x: x.sst)
    data.history[0] == "cdo -aexpr,'new=sst+273.15;old=sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + 273.15, old=lambda x: x.sst, drop=False)
    data.history[0] == "cdo -aexpr,'new=sst+273.15;old=sst'"

    data = nc.open_data(ff)
    data.assign(drop=False, new=lambda x: x.sst + 273.15, old=lambda x: x.sst)
    data.history[0] == "cdo -aexpr,'new=sst+273.15;old=sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x: x.sst + 273.15, drop=False, old=lambda x: x.sst)
    data.history[0] == "cdo -aexpr,'new=sst+273.15;old=sst'"

    data = nc.open_data(ff)
    with pytest.raises(ValueError):
        data.assign(x=1)

    with pytest.raises(ValueError):
        data.assign(y=lambda x: x.sst % 1)

    with pytest.raises(ValueError):
        data.assign(y=lambda x: x.sst // 1)

    with pytest.raises(ValueError):
        data.assign(x=1)

    with pytest.raises(ValueError):
        data.assign(drop=True)

    with pytest.raises(ValueError):
        data.assign()

    with pytest.raises(ValueError):
        data.assign(drop=1)

    with pytest.raises(ValueError):
        data.assign(x=1)

    with pytest.raises(ValueError):
        data.assign(y=lambda x: x.sst, x=1)
        data = nc.open_data(ff)

    data = nc.open_data(ff)
    data.assign(new=lambda x: np.mean([1][0] + 2) + x.sst)
    assert data.history[0] == "cdo -aexpr,'new=3.0+sst'"

    data = nc.open_data(ff)
    with pytest.raises(ValueError):
        data.assign(new=lambda x: pd.DataFrame({"x": [1]}) + x.sst)

    def fun():
        return "1"

    data = nc.open_data(ff)
    with pytest.raises(ValueError):
        data.assign(new=lambda x: fun() + x.sst)

    with pytest.raises(ValueError):
        data.assign(new=lambda x: spatial_mean(1))

    with pytest.raises(ValueError):
        data.assign(new=lambda x: [x.sst])

    with pytest.raises(ValueError):
        data.assign(new=lambda x: [sst])

    with pytest.raises(ValueError):
        data.assign(new=lambda x: ["x"][0])

    with pytest.raises(ValueError):
        data.assign(new=lambda x: x.sst ^ 2)

    data = nc.open_data(ff)
    data.assign(new=lambda x1: [1][0] + x1.sst)
    assert data.history[0] == "cdo -aexpr,'new=1+sst'"
    data = nc.open_data(ff)
    data.assign(new=lambda x1: np.mean(list({2, 1})) + x1.sst)
    assert data.history[0] == "cdo -aexpr,'new=1.5+sst'"

    data = nc.open_data(ff)
    data.assign(new=lambda x1: np.mean(list({2, 1})) + x1.sst)
    assert data.history[0] == "cdo -aexpr,'new=1.5+sst'"

    data = nc.open_data(ff)

    class MyClass:
        t = "1"

    k = MyClass()
    with pytest.raises(ValueError):
        data.assign(new=lambda x: x.sst + k.t)

    k = "a"
    with pytest.raises(ValueError):
        data.assign(new=lambda x: x.sst + k)

    k = ["a"]
    with pytest.raises(ValueError):
        data.assign(new=lambda x: x.sst + k)

    with pytest.raises(ValueError):
        data.assign(new=lambda x: x.sst + b)

    with pytest.raises(ValueError):
        data.assign(new=lambda x: 1)

    with pytest.raises(ValueError):
        data.assign(new=lambda x: a.s)

    class MyClass:
        t = [1]

    k = MyClass()
    with pytest.raises(ValueError):
        data.assign(new=lambda x: x.sst + k.t)

    data = nc.open_data("data/sst.mon.mean.nc")
    # data.select(time = 0 )
    data.assign(new=lambda x: (x.sst == x.sst) * timestep(x.sst + 1), old=lambda x: x.sst + timestep(x.sst))

    assert (
        data.history[0]
        == "cdo -aexpr,'new=(sst==sst)*(ctimestep(sst+1)-1);old=sst+(ctimestep(sst)-1)'"
    )

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: vertical_mean(x.sst + 100))
    assert data.history[0] == "cdo -aexpr,'new=vertmean(sst+100)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    with pytest.raises(ValueError):
        data.assign(new=lambda x: cell_area(x.sst + 100))

    with pytest.raises(ValueError):
        data.assign(new=lambda x: longitude(x.sst + 100))

    with pytest.raises(ValueError):
        data.assign(new=lambda x: latitude(x.sst + 100))

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: cell_area(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=gridarea(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: cell_area(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=gridarea(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: level(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=clev(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: longitude(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=clon(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: latitude(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=clat(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: lon(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=clon(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: lat(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=clat(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: second(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=csecond(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: minute(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=cminute(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: hour(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=chour(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: day(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=cday(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: month(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=cmonth(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: year(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=cyear(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: log(x.sst) * x.sst)
    assert data.history[0] == "cdo -aexpr,'new=ln(sst)*sst'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - zonal_mean(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-zonmean(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - zonal_max(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-zonmax(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - zonal_min(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-zonmin(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - zonal_sum(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-zonsum(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    with pytest.raises(ValueError):
        data.assign(new=lambda x: x.sst - zonal_range(x.sst))

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - vertical_mean(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-vertmean(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - vertical_max(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-vertmax(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - vertical_min(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-vertmin(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - vertical_sum(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-vertsum(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    with pytest.raises(ValueError):
        data.assign(new=lambda x: x.sst - vertical_range(x.sst))

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - spatial_mean(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-fldmean(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - spatial_max(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-fldmax(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - spatial_min(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-fldmin(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: x.sst - spatial_sum(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sst-fldsum(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: arctan(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=atan(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: arccos(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=acos(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: arcsin(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=asin(sst)'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: ((x.sst > 1 & x.sst < 10)))
    assert data.history[0] == "cdo -aexpr,'new=((sst>1&&sst<10))'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(new=lambda x: ((x.sst > 1 | x.sst < 10)))
    assert data.history[0] == "cdo -aexpr,'new=((sst>1||sst<10))'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(one2ten=lambda x: x.sst > 1 and x.sst < 10)
    assert data.history[0] == "cdo -aexpr,'one2ten=sst>1&&sst<10'"

    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(one2ten=lambda x: x.sst > 1 or x.sst < 10)
    assert data.history[0] == "cdo -aexpr,'one2ten=sst>1||sst<10'"


    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(one2ten=lambda x: abs(x.sst + 1) - abs(x.sst-1))
    assert data.history[0] == "cdo -aexpr,'one2ten=abs(sst+1)-abs(sst-1)'"


    data = nc.open_data("data/sst.mon.mean.nc")
    data.assign(one2ten           =              lambda          x         :          abs(          x.sst + 1      ) - abs(        x.sst-1       )        )
    assert data.history[0] == "cdo -aexpr,'one2ten=abs(sst+1)-abs(sst-1)'"


    del data



    ds1 = nc.open_data("data/woa18_decav_t01_01.nc")
    ds1.select(variables = "t_an")
    ds1.vertical_mean()

    
    ds2 = nc.open_data("data/woa18_decav_t01_01.nc")
    ds2.assign(t_an = lambda x: x.t_an/vertical_mean(x.t_an))
    ds2.surface()
    ds2.run()

    ds3 = nc.open_data("data/woa18_decav_t01_01.nc")
    ds3.surface()
    ds3.divide(ds1)
    ds3.run()

    ds2.spatial_mean()
    ds3.spatial_mean()

    x = ds2.to_dataframe().t_an.values[0]
    y = ds3.to_dataframe().t_an.values[0]


    assert x ==y

    del ds1
    del ds2
    del ds3



    ds = nc.open_data("data/sst.mon.mean.nc")
    ds.select(time = 0)
    ds.spatial_mean()
    x = ds.to_dataframe().sst.values[0]

    ds = nc.open_data("data/sst.mon.mean.nc")
    ds.select(time = 0)
    ##ds.assign(sst = lambda x: x.sst + spatial_mean(x.sst)*(isnan(x.sst)<1))
    ds.assign(sst = lambda x: x.sst + spatial_mean(x.sst))
    ds.spatial_mean()
    y = ds.to_dataframe().sst.values[0]


    assert 2*x == y
    del ds


