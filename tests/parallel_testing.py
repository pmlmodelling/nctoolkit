
import os

import nctoolkit as nc
nc.options(parallel = True)


for i in range(0, 5):
    def process_chain(ff):

        data = nc.open_data(ff)
        data.run()
        data.add(1)
        data.run()
        data.add(ff)
        data.run()
        data.to_nc(nc.temp_file.temp_file(".nc"), overwrite = True)


    import multiprocessing
    pool = multiprocessing.Pool(3)
    ensemble = nc.create_ensemble("data/ensemble")

    results = dict()
    target_list = []

    for f in ensemble:
        temp = pool.apply_async(process_chain, [f])
        results[f] = temp
    pool.close()
    pool.join()

    for k, v in results.items():
        target_list.append(v.get())



    def process_chain(ff):

        data = nc.open_data(ff)
        data.annual_anomaly(baseline = [1980,1989])
        data.to_nc(nc.temp_file.temp_file(".nc"), overwrite = True)


    import multiprocessing
    pool = multiprocessing.Pool(3)
    ensemble = [ "data/sst.mon.mean.nc", "data/sst.mon.mean.nc", "data/sst.mon.mean.nc"]


    results = dict()
    target_list = []

    for f in ensemble:
        temp = pool.apply_async(process_chain, [f])
        results[f] = temp
    pool.close()
    pool.join()

    for k, v in results.items():
        target_list.append(v.get())




    def process_chain(ff):

        data = nc.open_data(ff)
        data.assign(sst_k = lambda x: x.sst + 273.15)
        data.run()
        data.cdo_command("timmean")
        data.run()
        data.cell_area(join = True)
        data.run()
        data.cor_time("sst", "sst_k")
        data.run()
        data.to_nc(nc.temp_file.temp_file(".nc"), overwrite = True)


    import multiprocessing
    pool = multiprocessing.Pool(3)


    results = dict()
    target_list = []

    for f in ensemble:
        temp = pool.apply_async(process_chain, [f])
        results[f] = temp
    pool.close()
    pool.join()

    for k, v in results.items():
        target_list.append(v.get())



    def process_chain(ff):

        data = nc.open_data(ff)
        data.assign(sst_k = lambda x: x.sst + 273.15)
        data.run()
        data.nco_command("ncks -d lon,-10.0,10.0 -d lat,40.0,80.0")
        data.run()
        data.centre("latitude")
        data.run()
        data.to_nc(nc.temp_file.temp_file(".nc"), overwrite = True)


    import multiprocessing
    pool = multiprocessing.Pool(3)

    ensemble = nc.create_ensemble("data/ensemble")

    results = dict()
    target_list = []

    for f in ensemble:
        temp = pool.apply_async(process_chain, [f])
        results[f] = temp
    pool.close()
    pool.join()

    for k, v in results.items():
        target_list.append(v.get())




    def process_chain(ff):

        data = nc.open_data(ff)
        data.assign(sst_k = lambda x: x.sst + 273.15)
        data.run()
        data.crop(lon = [-10, 10], lat = [40, 80], nco = True)
        data.run()
        data.centre("latitude")
        data.run()
        data.to_nc(nc.temp_file.temp_file(".nc"), overwrite = True)


    import multiprocessing
    pool = multiprocessing.Pool(3)

    ensemble = nc.create_ensemble("data/ensemble")

    for f in ensemble:
        temp = pool.apply_async(process_chain, [f])
        results[f] = temp
    pool.close()
    pool.join()

    for k, v in results.items():
        target_list.append(v.get())




    def process_chain(ff):

        data = nc.open_data(ff)
        data.assign(sst_k = lambda x: x.sst + 273.15)
        data.run()
        data.cor_time("sst", "sst_k")
        data.to_nc(nc.temp_file.temp_file(".nc"), overwrite = True)


    import multiprocessing
    pool = multiprocessing.Pool(3)

    ensemble = nc.create_ensemble("data/ensemble")

    for f in ensemble:
        temp = pool.apply_async(process_chain, [f])
        results[f] = temp
    pool.close()
    pool.join()

    for k, v in results.items():
        target_list.append(v.get())



    def process_chain(ff):

        data = nc.open_data(ff)
        data.tmean()
        data.ensemble_mean()
        data.to_nc(nc.temp_file.temp_file(".nc"), overwrite = True)


    import multiprocessing
    pool = multiprocessing.Pool(3)

    ensemble = nc.create_ensemble("data/ensemble")
    big_ensemble = [ensemble, ensemble, ensemble, ensemble, ensemble]


    for f in big_ensemble:
        temp = pool.apply_async(process_chain, [f])
        results[f[0]] = temp
    pool.close()
    pool.join()

    for k, v in results.items():
        target_list.append(v.get())




    def process_chain(ff):

        data = nc.open_data(ff)
        data.assign(sst = lambda x: x.analysed_sst + 273.15)
        data.run()
        data.phenology("sst", "peak")
        data.to_nc(nc.temp_file.temp_file(".nc"), overwrite = True)


    import multiprocessing
    pool = multiprocessing.Pool(3)

    ensemble = ["data/2003.nc", "data/2003.nc", "data/2003.nc"]

    for f in ensemble:
        temp = pool.apply_async(process_chain, [f])
        results[f] = temp
    pool.close()
    pool.join()

    for k, v in results.items():
        target_list.append(v.get())




    def process_chain(ff):

        data = nc.open_data(ff)
        data.assign(sst = lambda x: x.sst + 273.15)
        data.run()
        data.tpercentile(50)
        data.to_nc(nc.temp_file.temp_file(".nc"), overwrite = True)


    import multiprocessing
    pool = multiprocessing.Pool(3)

    ensemble = nc.create_ensemble("data/ensemble")

    for f in ensemble:
        temp = pool.apply_async(process_chain, [f])
        results[f] = temp
    pool.close()
    pool.join()

    for k, v in results.items():
        target_list.append(v.get())





