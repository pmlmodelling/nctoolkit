wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4/hdf5-1.8.13.tar.gz
tar -xvf hdf5-1.8.13.tar.gz
cd hdf5-1.8.13/
./configure -with-zlib=/opt/cdo-install -prefix=/opt/cdo-install CFLAGS=-fPIC

sudo make
sudo make install> /dev/null
cd ..

wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.4.0.tar.gz
tar -xvf netcdf-4.4.0.tar.gz
cd netcdf-4.4.0/
CPPFLAGS=-I/opt/cdo-install/include LDFLAGS=-L/opt/cdo-install/lib ./configure -prefix=/opt/cdo-install CFLAGS=-fPIC
sudo make  > /dev/null
sudo make install > /dev/null

cd ..


wget https://code.mpimet.mpg.de/attachments/download/17374/cdo-1.9.4.tar.gz
tar -xvzf cdo-1.9.4.tar.gz
cd cdo-1.9.4
./configure -with-netcdf=/opt/cdo-install -with-hdf5=/opt/cdo-install
sudo make
sudo make install
cd ..
