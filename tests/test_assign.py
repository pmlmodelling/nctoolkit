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


    ff = "data/sst.mon.mean.nc"


    # In[4]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: x.sst + 273.15)
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[5]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: x.sst + [273.15][0])
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[6]:


    data = nc.open_data(ff)
    k = [273.15]
    data.assign(new = lambda x: x.sst + k[0])
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[7]:


    data = nc.open_data(ff)
    k = [273.15]
    data.assign(new = lambda x: x.sst + k[0])
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[8]:


    data = nc.open_data(ff)
    k = 273.15
    data.assign(new = lambda x: x.sst + k)
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[9]:


    data = nc.open_data(ff)
    k = 273.15
    data.assign(new = lambda x: x.sst + pd.DataFrame({"x":[273.15]}).x[0])
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[10]:


    data = nc.open_data(ff)
    k = 273.15
    class MyClass():
        t = 273.15
    k = MyClass()
    data.assign(new = lambda x:      x.sst     +     k.t  )
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[11]:


    data = nc.open_data(ff)
    k = 273.15
    data.assign(new = lambda x:      x.sst     +   np.mean(k))
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[12]:


    data = nc.open_data(ff)
    k = [273.15]
    data.assign(new = lambda x:      x.sst     +   np.mean(k))
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[13]:


    data = nc.open_data(ff)
    k = [273.15, 273.15]
    data.assign(new = lambda x:      x.sst     +   np.mean(k))
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"


    # In[14]:


    data = nc.open_data(ff)
    k = [273.15, 273.15]
    data.assign(new = lambda x: x.sst + np.mean([273.15]))
    assert data.history[0] == "cdo -aexpr,'new=sst+273.15'"




    # In[3]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: x.sst **2)
    assert data.history[0] == "cdo -aexpr,'new=sst^2'"


    # In[4]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst > 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst>2)'"


    # In[ ]:





    # In[5]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst < 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst<2)'"


    # In[6]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst <= 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst<=2)'"


    # In[7]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst >= 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst>=2)'"



    # In[8]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst == 2))
    assert data.history[0] == "cdo -aexpr,'new=(sst==2)'"


    # In[9]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst > 2) | (x.sst < 10))
    assert data.history[0] == "cdo -aexpr,'new=(sst>2)||(sst<10)'"


    # In[10]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst == 2) | (x.sst < 10))
    assert data.history[0] == "cdo -aexpr,'new=(sst==2)||(sst<10)'"


    # In[13]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst != 2) | (x.sst < 10))
    assert data.history[0] == "cdo -aexpr,'new=(sst!=2)||(sst<10)'"


    # In[16]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst != 2) & (x.sst < 10))
    assert data.history[0] == "cdo -aexpr,'new=(sst!=2)&&(sst<10)'"



    data = nc.open_data(ff)
    data.assign(new = lambda x: sqrt(x.sst))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst)'"


    # In[4]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: sqrt(x.sst +2))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst+2)'"


    # In[5]:


    data = nc.open_data(ff)
    k = 2
    data.assign(new = lambda x: sqrt(x.sst +k))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst+2)'"


    # In[6]:


    data = nc.open_data(ff)
    k = [2,1]
    data.assign(new = lambda x: sqrt(x.sst +k[0]))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst+2)'"


    # In[11]:


    data = nc.open_data(ff)
    k = [2,1,[2]]
    data.assign(new = lambda x: sqrt(x.sst +k[2][0]))
    assert data.history[0] == "cdo -aexpr,'new=sqrt(sst+2)'"



    # In[17]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: x.sst+ x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst+sst'"


    # In[19]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: x.sst- x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst-sst'"


    # In[20]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: x.sst* x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst*sst'"


    # In[27]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: x.sst/ x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst/sst'"


    # In[28]:


    data = nc.open_data(ff)
    data.assign(new = lambda x: x.sst**x.sst)
    assert  data.history[0] == "cdo -aexpr,'new=sst^sst'"

    data = nc.open_data(ff)
    data.assign(new = lambda x: (x.sst+ x.sst))
    assert data.history[0] == "cdo -aexpr,'new=(sst+sst)'"


    data = nc.open_data(ff)
    data.assign(new = lambda x: ((x.sst+ x.sst) + np.mean(2)))
    assert data.history[0] == "cdo -aexpr,'new=((sst+sst)+2.0)'"


    data = nc.open_data(ff)
    data.assign(new = lambda x:  x.sst + np.mean(2) + np.mean(2) + np.mean(2))
    assert data.history[0] == "cdo -aexpr,'new=sst+2.0+2.0+2.0'"



    data = nc.open_data(ff)
    data.assign(new = lambda x:  x.sst + np.mean(2) + np.mean(2) + np.mean(2)-x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst+2.0+2.0+2.0-sst'"

    data = nc.open_data(ff)
    data.assign(new = lambda x:  x.sst + np.mean(np.mean(2)) + np.mean(2) + np.mean(2)-x.sst)
    assert data.history[0] == "cdo -aexpr,'new=sst+2.0+2.0+2.0-sst'"




