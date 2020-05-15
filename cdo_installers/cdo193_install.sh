wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4/hdf5-1.8.13.tar.gz
tar -xvf hdf5-1.8.13.tar.gz
cd hdf5-1.8.13/
./configure -with-zlib=/opt/cdo-install -prefix=/opt/cdo-install CFLAGS=-fPIC

make
make install
cd ..

wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.4.0.tar.gz
tar -xvf netcdf-4.4.0.tar.gz
cd netcdf-4.4.0/
CPPFLAGS=-I/opt/cdo-install/include LDFLAGS=-L/opt/cdo-install/lib ./configure -prefix=/opt/cdo-install CFLAGS=-fPIC
make
make install

cd ..


wget https://code.mpimet.mpg.de/attachments/download/16435/cdo-1.9.3.tar.gz
tar -xvzf cdo-1.9.3.tar.gz
cd cdo-1.9.3
./configure -with-netcdf=/opt/cdo-install -with-hdf5=/opt/cdo-install
make
make install
cd ..
