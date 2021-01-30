
import os

import nctoolkit as nc
nc.options(parallel = True)
def process_chain(ff):

    data = nc.open_data(ff)
    data.add(1)
    data.add(ff)
    data.run()

    nc.session.append_safe(data.current[0])

import multiprocessing
pool = multiprocessing.Pool(3)
ensemble = nc.create_ensemble("data/ensemble")

for f in ensemble:
    pool.apply_async(process_chain, [f])
pool.close()
pool.join()


if len(ensemble) != len(nc.session_files()):
    raise ValueError("problem processing file")


if len(nc.session.get_safe()) != len(nc.session_files()):
    raise ValueError("problem processing file")


