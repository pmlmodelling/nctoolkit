import nctoolkit as nc

ds = nc.open_data("data/sst.mon.mean.nc")
ds.tmean()
ds.run()
