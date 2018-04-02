
# coding: utf-8

# In[ ]:


import numpy as np
import numpy.ma as ma
import os
import xarray as xr
import glob
import loadobservations as lo
import esio

# TODO: use stereo_gridinfo.nc ?

# Dirs
data_dir = r'/home/disk/sipn/nicway/data/obs'

product_list = ['NSIDC_0081', 'NSIDC_0051' , 'NSIDC_0079']

# Loop through each product
for c_product in product_list:

    c_data_dir = os.path.join(data_dir, c_product, 'native', '*.bin')
    all_files = sorted(glob.glob(c_data_dir))
    out_dir = os.path.join(data_dir, c_product, 'sipn_nc')

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Load in 
    ds_sic = lo.load_NSIDC(all_files=all_files, product=c_product)

    # Add lat and lon dimensions
    ds_lat_lon = esio.get_stero_N_grid()
    ds_sic.coords['lat'] = ds_lat_lon.lat
    ds_sic.coords['lon'] = ds_lat_lon.lon
    
    # Stereo projected units (m)
    dx = dy = 25000 
    xm = np.arange(-3850000, +3750000, +dx)
    ym = np.arange(+5850000, -5350000, -dy)
    ds_sic.coords['xm'] = xr.DataArray(xm, dims=('x'))
    ds_sic.coords['ym'] = xr.DataArray(ym, dims=('y'))    

    # Save to netcdf file
    out_nc = c_product+'.nc'
    ds_sic.to_netcdf(os.path.join(out_dir,out_nc))
    print("Saved ",out_nc)
    print(ds_sic)
    ds_sic = None


