import nctoolkit as nc
import pandas as pd
import xarray as xr
import os, pytest
import subprocess

nc.options(lazy=True)


def cdo_version():
    cdo_check = subprocess.run(
        "cdo --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    cdo_check = str(cdo_check.stderr).replace("\\n", "")
    cdo_check = cdo_check.replace("b'", "").strip()
    return cdo_check.split("(")[0].strip().split(" ")[-1]


ff = "data/sst.mon.mean.nc"
ensemble = nc.create_ensemble("data/ensemble")


class TestCalls:
    def test_cellcall(self):
        data = nc.open_data(ff)
        data.cell_area(join=False)

        assert data.history[0] == 'cdo -setattribute,cell_area@units="m^2" -gridarea'

        data = nc.open_data(ff)
        data.cell_area(join=True)

        if cdo_version() in ["1.9.2", "1.9.3", "1.9.4", "1.9.5", "1.9.6"]:
            print(data.history)
            assert len(data.history) == 3
            assert "cdo -L -merge data/sst.mon.mean.nc" in data.history[1]
            assert "cdo -L -gridarea data/sst.mon.mean.nc" in data.history[0]
            assert 'cdo -L -setattribute,cell_area@units="m^2' in data.history[2]
        else:
            assert len(data.history) == 2
            assert "cdo -L -merge data/sst.mon.mean.nc" in data.history[0]
            assert "-gridarea data/sst.mon.mean.nc" in data.history[0]
            assert 'cdo -L -setattribute,cell_area@units="m^2' in data.history[1]

    def test_cropcall(self):
        nc.options(lazy=True)
        data = nc.open_data(ff)
        data.crop(lon=[0, 90], lat=[0, 90])

        assert data.history[0] == "cdo -L -sellonlatbox,0,90,0,90"

    def test_selectvariablescall(self):
        nc.options(lazy=True)
        data = nc.open_data(ff)
        data.select(variables="sst")

        assert data.history[0] == "cdo -selname,sst"
        data = nc.open_data(ff)
        data.select(variables=["sst", "tos"])
        assert data.history[0] == "cdo -selname,sst,tos"

    def test_selecttimestepcall(self):
        nc.options(lazy=True)
        data = nc.open_data(ff)
        data.select(timesteps=0)

        assert data.history[0] == "cdo -seltimestep,1"



    def test_sumallcall(self):
        nc.options(lazy=True)
        data = nc.open_data(ff)
        data.assign(k = lambda x: x.sst+273.15)
        data.sum_all()

        assert data.history[1] == 'cdo -expr,total=k+sst '

    def test_selectseasoncall(self):
        nc.options(lazy=True)
        data = nc.open_data(ff)
        data.select(seasons="DJF")

        assert data.history[0] == "cdo -select,season=DJF"

    def test_selectmonthcall(self):
        nc.options(lazy=True)
        data = nc.open_data(ff)
        data.select(months=range(1, 3))

        assert data.history[0] == "cdo -selmonth,1,2"

    def test_selectyearscall(self):
        nc.options(lazy=True)
        data = nc.open_data(ff)
        data.select(years=range(1970, 1973))

        assert data.history[0] == "cdo -selyear,1970,1971,1972"

    def test_callchecks(self):
        nc.options(lazy=True)

        # zonal statistics

        data = nc.open_data(ff)
        data.zonal_mean()
        assert data.history[0] == "cdo -zonmean"

        data = nc.open_data(ff)
        data.zonal_min()
        assert data.history[0] == "cdo -zonmin"

        data = nc.open_data(ff)
        data.zonal_max()
        assert data.history[0] == "cdo -zonmax"

        data = nc.open_data(ff)
        data.zonal_range()
        assert data.history[0] == "cdo -zonrange"

        # meridonial statistics

        data = nc.open_data(ff)
        data.meridonial_mean()
        assert data.history[0] == "cdo -mermean"

        data = nc.open_data(ff)
        data.meridonial_min()
        assert data.history[0] == "cdo -mermin"

        data = nc.open_data(ff)
        data.meridonial_max()
        assert data.history[0] == "cdo -mermax"

        data = nc.open_data(ff)
        data.meridonial_range()
        assert data.history[0] == "cdo -merrange"

        # seasonal mean

        data = nc.open_data(ff)
        data.tmean(["year", "season"])

        assert data.history[0] == "cdo -seasmean"

        data = nc.open_data(ff)
        data.tmin(["year", "season"])

        assert data.history[0] == "cdo -seasmin"

        data = nc.open_data(ff)
        data.tmax(["year", "season"])

        assert data.history[0] == "cdo -seasmax"

        data = nc.open_data(ff)
        data.trange(["year", "season"])

        assert data.history[0] == "cdo -seasrange"

        data = nc.open_data(ff)
        data.tmean("season")
        assert data.history[0] == "cdo -yseasmean"

        data = nc.open_data(ff)
        data.tmin("season")
        assert data.history[0] == "cdo -yseasmin"

        data = nc.open_data(ff)
        data.tmax("season")
        assert data.history[0] == "cdo -yseasmax"

        data = nc.open_data(ff)
        data.trange("season")
        assert data.history[0] == "cdo -yseasrange"

        data = nc.open_data(ff)
        data.tmean("year")
        assert data.history[0] == "cdo -yearmean"

        data = nc.open_data(ff)
        data.tmin("year")
        assert data.history[0] == "cdo -yearmin"

        data = nc.open_data(ff)
        data.tmax("year")
        assert data.history[0] == "cdo -yearmax"

        data = nc.open_data(ff)
        data.trange("year")
        assert data.history[0] == "cdo -yearrange"

        data = nc.open_data(ff)
        data.tsum("year")
        assert data.history[0] == "cdo -yearsum"

        # daily stats

        data = nc.open_data(ff)
        data.tmean(["year", "day"])
        assert data.history[0] == "cdo -daymean"

        data = nc.open_data(ff)
        data.tmin(["year", "day"])
        assert data.history[0] == "cdo -daymin"

        data = nc.open_data(ff)
        data.tmax(["year", "day"])
        assert data.history[0] == "cdo -daymax"

        data = nc.open_data(ff)
        data.trange(["year", "day"])
        assert data.history[0] == "cdo -dayrange"

        data = nc.open_data(ff)
        data.tsum(["year", "day"])
        assert data.history[0] == "cdo -daysum"

        data = nc.open_data(ff)
        data.timestep_interp(2)
        assert data.history[0] == "cdo -intntime,2"

        data = nc.open_data(ff)
        data.tmean(["year", "month"])
        assert data.history[0] == "cdo -monmean"

        data = nc.open_data(ff)
        data.tmin(["year", "month"])
        assert data.history[0] == "cdo -monmin"

        data = nc.open_data(ff)
        data.tmax(["year", "month"])
        assert data.history[0] == "cdo -monmax"

        data = nc.open_data(ff)
        data.trange(["year", "month"])
        assert data.history[0] == "cdo -monrange"

        data = nc.open_data(ff)
        data.tmean("month")
        assert data.history[0] == "cdo -ymonmean"

        data = nc.open_data(ff)
        data.tmin("month")
        assert data.history[0] == "cdo -ymonmin"

        data = nc.open_data(ff)
        data.tmax("month")
        assert data.history[0] == "cdo -ymonmax"

        data = nc.open_data(ff)
        data.trange("month")
        assert data.history[0] == "cdo -ymonrange"

        data = nc.open_data(ff)
        data.tmean("day")
        assert data.history[0] == "cdo -ydaymean"

        data = nc.open_data(ff)
        data.tmin("day")
        assert data.history[0] == "cdo -ydaymin"

        data = nc.open_data(ff)
        data.tmax("day")
        assert data.history[0] == "cdo -ydaymax"

        data = nc.open_data(ff)
        data.trange("day")
        assert data.history[0] == "cdo -ydayrange"

        data = nc.open_data(ff)
        data.rename({"sst": "tos"})

        assert data.history[0] == "cdo -chname,sst,tos"

        data = nc.open_data(ff)
        data.set_units({"sst": "tos"})
        assert data.history[0] == 'cdo -setattribute,sst@units="tos"'

        data = nc.open_data(ff)
        data.set_missing([0, 0])
        assert data.history[0] == "cdo -setrtomiss,0,0"

        data = nc.open_data(ff)
        data.tmean()
        assert data.history[0] == "cdo -timmean"

        data = nc.open_data(ff)
        data.tmax()
        assert data.history[0] == "cdo -timmax"

        data = nc.open_data(ff)
        data.tmin()
        assert data.history[0] == "cdo -timmin"

        data = nc.open_data(ff)
        data.trange()
        assert data.history[0] == "cdo -timrange"

        data = nc.open_data(ff)
        data.tsum()
        assert data.history[0] == "cdo -timsum"

        data = nc.open_data(ff)
        data.tvariance()
        assert data.history[0] == "cdo -timvar"

        data = nc.open_data(ff)
        data.tstdev()
        assert data.history[0] == "cdo -timstd"

        data = nc.open_data(ff)
        data.tcumsum()
        assert data.history[0] == "cdo -timcumsum"

        data = nc.open_data(ff)
        data.tpercentile(p=1)
        assert (
            "cdo -L -timpctl,1 data/sst.mon.mean.nc -timmin data/sst.mon.mean.nc -timmax data/sst.mon.mean.nc"
            in data.history[0]
        )

        data = nc.open_data(ff)
        data.drop("sst")
        assert data.history[0] == "cdo -delete,name=sst"

        if cdo_version() not in ["1.9.2", "1.9.3"]:
            data = nc.open_data(ensemble)
            data.merge_time()
            assert data.history[0] == "cdo --sortname -mergetime"

        data = nc.open_data(ff)
        data.rolling_mean(10)
        assert data.history[0] == "cdo -runmean,10"

        data = nc.open_data(ff)
        data.rolling_min(10)
        assert data.history[0] == "cdo -runmin,10"

        data = nc.open_data(ff)
        data.rolling_max(10)
        assert data.history[0] == "cdo -runmax,10"

        data = nc.open_data(ff)
        data.rolling_range(10)
        assert data.history[0] == "cdo -runrange,10"

        data = nc.open_data(ff)
        data.rolling_sum(10)
        assert data.history[0] == "cdo -runsum,10"

        if cdo_version() not in ["1.9.2", "1.9.3"]:
            data = nc.open_data(ff)
            data.spatial_mean()
            assert data.history[0] == "cdo -fldmean"

            data = nc.open_data(ff)
            data.spatial_max()
            assert data.history[0] == "cdo -fldmax"

            data = nc.open_data(ff)
            data.spatial_min()
            assert data.history[0] == "cdo -fldmin"

            data = nc.open_data(ff)
            data.spatial_range()
            assert data.history[0] == "cdo -fldrange"

            data = nc.open_data(ff)
            data.spatial_sum()
            assert data.history[0] == "cdo -fldsum"

            data = nc.open_data(ff)
            data.spatial_percentile(1)
            assert data.history[0] == "cdo -fldpctl,1"

        data = nc.open_data(ff)
        data.cor_time("sst", "sst")
        assert len(data.history) == 3
        assert (
            "cdo -L -timcor -selname,sst data/sst.mon.mean.nc -selname,sst data/sst.mon.mean.nc"
            in data.history[0]
        )
        assert 'cdo -L -setattribute,cor@units="-" -chname,sst,cor' in data.history[1]
        assert (
            'ncatted -a long_name,cor,o,c,"Correlation between sst & sst"'
            in data.history[2]
        )

        data = nc.open_data(ff)
        data.cor_space("sst", "sst")
        assert len(data.history) == 3
        assert (
            "cdo -L -fldcor -selname,sst data/sst.mon.mean.nc -selname,sst data/sst.mon.mean.nc"
            in data.history[0]
        )
        assert 'cdo -L -setattribute,cor@units="-" -chname,sst,cor' in data.history[1]
        assert (
            'ncatted -a long_name,cor,o,c,"Correlation between sst & sst"'
            in data.history[2]
        )

        data = nc.open_data(ff)
        data.split("year")
        assert "cdo -s -splityear data/sst.mon.mean.nc" in data.history[0]

        data = nc.open_data(ff)
        data.annual_anomaly(baseline=[1970, 1979], window=10)
        assert (
            "cdo -L -sub -runmean,10 -yearmean data/sst.mon.mean.nc -timmean -selyear,1970/1979 data/sst.mon.mean.nc"
            in data.history[0]
        )

        data = nc.open_data(ff)
        data.monthly_anomaly(baseline=[1970, 1979])
        assert (
            "cdo -L -ymonsub -monmean data/sst.mon.mean.nc -ymonmean -selyear,1970/1979 data/sst.mon.mean.nc"
            in data.history[0]
        )

        data = nc.open_data(ff)
        data.compare("<0")
        assert data.history[0] == "cdo -ltc,0"

        data = nc.open_data(ff)
        data.compare("==0")
        assert data.history[0] == "cdo -eqc,0"

        data = nc.open_data(ff)
        data.compare("!=0")
        assert data.history[0] == "cdo -nec,0"

        data = nc.open_data(ff)
        data.compare("<=0")
        assert data.history[0] == "cdo -lec,0"

        data = nc.open_data(ff)
        data.compare("<0")
        assert data.history[0] == "cdo -ltc,0"

        data = nc.open_data(ff)
        data.compare("<-1")
        assert data.history[0] == "cdo -ltc,-1"


        data = nc.open_data(ff)
        data.compare(">=0")
        assert data.history[0] == "cdo -gec,0"

        data = nc.open_data(ff)
        data.compare(">=-1")
        assert data.history[0] == "cdo -gec,-1"


        data = nc.open_data(ff)
        data.compare(">-1")
        assert data.history[0] == "cdo -gtc,-1"

        data = nc.open_data(ff)
        data.compare(">1")
        assert data.history[0] == "cdo -gtc,1"



        data = nc.open_data(ff)
        data.compare("!=-1")
        assert data.history[0] == "cdo -nec,-1"

        data = nc.open_data(ff)
        data.compare("<=-1")
        assert data.history[0] == "cdo -lec,-1"

        data = nc.open_data(ff)

        with pytest.raises(ValueError):
            data.compare("e")

        with pytest.raises(ValueError):
            data.compare("==e")

        with pytest.raises(ValueError):
            data.compare()

        with pytest.raises(TypeError):
            data.compare(1)

        with pytest.raises(ValueError):
            data.compare(">=e")
        with pytest.raises(ValueError):
            data.compare(">=-e")
        with pytest.raises(ValueError):
            data.compare(">e")
        with pytest.raises(ValueError):
            data.compare(">-e")

        with pytest.raises(ValueError):
            data.compare("!=e")
        with pytest.raises(ValueError):
            data.compare("!=-e")

        with pytest.raises(ValueError):
            data.compare("<=e")
        with pytest.raises(ValueError):
            data.compare("<=-e")



        with pytest.raises(ValueError):
            data.compare("==-e")
        with pytest.raises(ValueError):
            data.compare("<-e")
        with pytest.raises(ValueError):
            data.compare(">-e")
        with pytest.raises(ValueError):
            data.compare("<=e")
        with pytest.raises(ValueError):
            data.compare(">=-e")
        with pytest.raises(ValueError):
            data.compare("<e")




        data = nc.open_data(ff)
        data.compare("==-1")
        assert data.history[0] == "cdo -eqc,-1"

        data = nc.open_data(ff)
        data.add(1)
        assert data.history[0] == "cdo -addc,1"

        data = nc.open_data(ff)
        data.subtract(1)
        assert data.history[0] == "cdo -subc,1"

        data = nc.open_data(ff)
        data.multiply(1)
        assert data.history[0] == "cdo -mulc,1"

        data = nc.open_data(ff)
        data.divide(1)
        assert data.history[0] == "cdo -divc,1"

        if cdo_version() not in ["1.9.2", "1.9.3"]:
            data = nc.open_data(ff)
            data.add(data)
            assert data.history[0] == "cdo -add  infile09178 data/sst.mon.mean.nc"

            data = nc.open_data(ff)
            data.subtract(data)
            assert data.history[0] == "cdo -sub  infile09178 data/sst.mon.mean.nc"

            data = nc.open_data(ff)
            data.multiply(data)
            assert data.history[0] == "cdo -mul  infile09178 data/sst.mon.mean.nc"

            data = nc.open_data(ff)
            data.divide(data)
            assert data.history[0] == "cdo -div  infile09178 data/sst.mon.mean.nc"

        data = nc.open_data(ff)
        data.set_date(year=1990, month=10, day=1)
        assert data.history[0] == "cdo -setreftime,1900-01-01 -setdate,1990-10-1"

        data = nc.open_data(ff)
        data.set_longnames({"sst": "long"})
        assert (
            'ncatted -a long_name,sst,o,c,"long" data/sst.mon.mean.nc'
            in data.history[0]
        )

        ff1 = "data/woa18_decav_t01_01.nc"

        data = nc.open_data(ff1)
        data.vertical_mean()
        assert data.history[0] == "cdo -vertmean"

        data = nc.open_data(ff1)
        data.vertical_min()
        assert data.history[0] == "cdo -vertmin"

        data = nc.open_data(ff1)
        data.vertical_max()
        assert data.history[0] == "cdo -vertmax"

        data = nc.open_data(ff1)
        data.vertical_range()
        assert data.history[0] == "cdo -vertrange"

        data = nc.open_data(ff1)
        data.vertical_sum()
        assert data.history[0] == "cdo -vertsum"

        data = nc.open_data(ff1)
        data.vertical_cumsum()
        assert data.history[0] == "cdo -vertcum"

        data = nc.open_data(ff1)
        data.surface()
        assert data.history[0] == "cdo -sellevidx,1"

        data = nc.open_data(ff1)
        data.bottom()
        assert data.history[0] == "cdo -sellevidx,57"

        data = nc.open_data(ff1)
        data.vertical_interp([1, 19])
        assert data.history[0] == "cdo -intlevel,1,19"

        data = nc.open_data(ff1)
        data.invert_levels()
        assert data.history[0] == "cdo -invertlev"

        data = nc.open_data(ff)
        data.mask_box(lon=[0, 90], lat=[0, 90])
        assert data.history[0] == "cdo -masklonlatbox,0,90,0,90"

        data = nc.open_data(ff)
        data.reduce_dims()
        assert data.history[0] == "cdo --reduce_dim copy"

        data = nc.open_data(ff1)
        data.surface()
        data.reduce_dims()
        assert data.history[0] == "cdo --reduce_dim -sellevidx,1"

        data = nc.open_data(ensemble)
        data.ensemble_mean(nco=True)
        assert "ncea -y mean" in data.history[0]

        data = nc.open_data(ensemble)
        data.ensemble_max(nco=True)
        assert "ncea -y max" in data.history[0]

        data = nc.open_data(ensemble)
        data.ensemble_min(nco=True)
        assert "ncea -y min" in data.history[0]

        data = nc.open_data(ensemble)
        data.ensemble_range()
        assert data.history[0] == "cdo --sortname -ensrange"

        data = nc.open_data(ensemble)
        data.ensemble_percentile(10)
        assert data.history[0] == "cdo --sortname -enspctl,10"


        data = nc.open_data(ff)
        data.shift(hours = -1)
        assert data.history[0] == "cdo -shifttime,-1hour"



        data = nc.open_data(ff)
        data.shift(months = -1)
        assert data.history[0] == "cdo -shifttime,-1months"


        data = nc.open_data(ff)
        data.shift(years = -1)
        assert data.history[0] == "cdo -shifttime,-1years"



