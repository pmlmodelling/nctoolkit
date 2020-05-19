
import nctoolkit as nc
from pathlib import Path


def test_plot_df1():
    ff = "data/sst.mon.mean.nc"
    data = nc.open_data(ff)
    data.plot()
    nc.session.html_files
    assert Path(nc.session.html_files[-1]).stat().st_size == 397027


