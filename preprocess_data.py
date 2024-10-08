#preprocess_data.py

import xarray as xr
import xesmf as xe
import numpy as np


def rename_dims_to_standard(ds):
    """
    Automatically detect and rename dimensions to the standard names: 'time', 'lat', 'lon'.
    
    ds (xarray.Dataset or xarray.DataArray): Input dataset or data array.
    
    """
    
    rename_dict = {}

    # Step 1: Detect longitude
    if 'lon' not in ds.dims:
        for possible_lon in ['longitude', 'x', 'lon', 'LONGITUDE', 'Longitude']:
            if possible_lon in ds.dims or possible_lon in ds.coords:
                rename_dict[possible_lon] = 'lon'
                break

    # Step 2: Detect latitude
    if 'lat' not in ds.dims:
        for possible_lat in ['latitude', 'y', 'lat', 'LATITUDE', 'Latitude']:
            if possible_lat in ds.dims or possible_lat in ds.coords:
                rename_dict[possible_lat] = 'lat'
                break

    # Step 3: Detect time
    if 'time' not in ds.dims:
        for possible_time in ['time', 't', 'TIME', 'Time']:
            if possible_time in ds.dims or possible_time in ds.coords:
                rename_dict[possible_time] = 'time'
                break

    # Step 4: Rename the detected dimensions
    if rename_dict:
        ds = ds.rename(rename_dict)
    
    return ds



def adjust_longitude(ds, lon_name='lon', to_range='0_360'):
    
    ''' Adjust the longitude values either from [-180, 180] to [0, 360] or from [0, 360] to [-180, 180].
    
    ds : Input dataset or data array.
    lon_name : Name of the longitude variable (default is 'lon').
    to_range : The target longitude range, either '0_360' or '-180_180'. '''
    
    lon = ds[lon_name]
    
    if to_range == '0_360':

        if lon.min() < 0:
            ds[lon_name] = lon.where(lon >= 0, lon + 360)
    elif to_range == '-180_180':

        if lon.max() > 180:
            ds[lon_name] = lon.where(lon <= 180, lon - 360)
    else:
        raise ValueError("Invalid target range. Use '0_360' or '-180_180'.")

    ds = ds.sortby(lon_name)
    
    return ds





# def load_data(path, var=None, start_time=None, end_time=None, lat_s=None, lat_e=None, lon_s=None, lon_e=None):

# 	''' This function loads the variables from nc files as xarray.DataArray 
# 		path: directory to nc file
# 		var : variables to be extracted
# 		start_time: start time for the variables to be extracted
# 		end_time: end time for the variables to be extracted   
# 		(end_time - start_time = time period for analysis)
# 		lat_s: start latitude
# 		lat_e: end latitude (check latitude order using ncdump -v lat ncfile.nc 
# 		lat_s and lat_e should be choosen in earlier and later latidues, in the 
# 		output of ncdump, both should be provided or none for global)
# 		lon_s: start longitude
# 		lon_e: end longitude (check longitude order using ncdump -v lon ncfile.nc 
# 		lon_s and lon_e should be choosen in order of earlier and later longidues, 
# 		in the output of ncdump, both should be provided or none for global)'''


#     if var == None:
#         return xr.open_dataset(path)

#     else:
#         if (start_time == None or end_time==None) and (lat_s==None or lat_e==None) and(lon_s==None or lon_e==None):
#             return xr.open_dataset(path)[var]
#         elif (lat_s==None or lat_e==None) and (lon_s==None or lon_e==None):
#             return xr.open_dataset(path)[var].sel(time=slice(f'{start_time}-01-01', f'{end_time}-12-30'))

#         elif (start_time == None or end_time==None) and(lon_s==None or lon_e==None):
#             return xr.open_dataset(path)[var].sel(lat=slice(lat_s, lat_e))

#         elif (start_time == None or end_time==None) and(lat_s==None or lat_e==None):
#             return xr.open_dataset(path)[var].sel(lon=slice(lon_s, lon_e))

#         elif (start_time == None or end_time==None):
#             return xr.open_dataset(path)[var].sel(lon=slice(lon_s, lon_e), lat=slice(lat_s, lat_e))
#         elif (lat_s==None or lat_e==None):
#             return xr.open_dataset(path)[var].sel(lon=slice(lon_s, lon_e), time=slice(f'{start_time}-01-01', f'{end_time}-12-30'))

#         elif (lon_s==None or lon_e==None):
#             return xr.open_dataset(path)[var].sel(lat=slice(lat_s, lat_e), time=slice(f'{start_time}-01-01', f'{end_time}-12-30'))

#         else:
#             return xr.open_dataset(path)[var].sel(lat=slice(lat_s, lat_e), time=slice(f'{start_time}-01-01', f'{end_time}-12-30'), lon=slice(lon_s, lon_e))


def load_data(path, var=None, start_time=None, end_time=None, lat_s=None, lat_e=None, lon_s=None, lon_e=None):
    """
    Load variables from NetCDF files as xarray.DataArray or Dataset.
    
    Parameters:
    -----------
    path : str
        Path to the NetCDF file.
    var : str, optional
        Variable name to extract from the file. If None, the entire dataset is returned.
    start_time : str, optional
        Start year in 'YYYY' format for the time range selection.
    end_time : str, optional
        End year in 'YYYY' format for the time range selection.
    lat_s : float, optional
        Start latitude for spatial selection. If None, the full latitude range is selected.
    lat_e : float, optional
        End latitude for spatial selection. If None, the full latitude range is selected.
    lon_s : float, optional
        Start longitude for spatial selection. If None, the full longitude range is selected.
    lon_e : float, optional
        End longitude for spatial selection. If None, the full longitude range is selected.

    Returns:
    --------
    xarray.DataArray or xarray.Dataset
        The selected subset of data based on the provided parameters.
    """
    

    ds = xr.open_dataset(path)
    

    if var:
        ds = ds[var]
    

    selection = {}


    if start_time and end_time:
        selection['time'] = slice(f'{start_time}-01-01', f'{end_time}-12-31')


    if lat_s is not None and lat_e is not None:
        selection['lat'] = slice(lat_s, lat_e)
    

    if lon_s is not None and lon_e is not None:
        selection['lon'] = slice(lon_s, lon_e)


    if selection:
        ds = ds.sel(**selection)
    
    return ds



def write_netcdf(data, file_path):
    """Save the given data to a NetCDF file.
    data: xarray.DataArray to be saved on netcdf format
    file_path: directory where file needs to be saved"""
    data.to_netcdf(file_path)
    print(f"Data saved to {file_path}")


import xarray as xr
import xesmf as xe

def regridding(ds, ds_out=None, var=None, method=None, to_range=None, x_s=None, x_e=None, x_i=None, y_s=None, y_e=None, y_i=None):
    '''
    This function is useful for regridding rectilinear and curvilinear grids.
    
    ds : xarray.Dataset or xarray.DataArray
        The dataset or dataarray containing the variable grid to be regridded.
        
    ds_out : xarray.Dataset or xarray.DataArray
        The target dataset or dataarray containing the target grid.
        if ds_out==None, regridding will be done using a generic grid made using xe, xs, ye, ys, xi and yi

        
    var :
        The name of the variable to be regridded. If None, it is assumed that `ds` and `ds_out` are DataArrays.
        
    to_range :
        The target longitude range, either '0_360' or '-180_180'. Default is '0_360'.
        
    method : str, optional
        The method for regridding. Default is 'bilinear'. Other values can be:
        ['bilinear', 'conservative', 'patch', 'conservative_normed', 'nearest_s2d', 'nearest_d2s'].
        For more details, see:
        - https://xesmf.readthedocs.io/en/stable/notebooks/Compare_algorithms.html
        - https://earthsystemmodeling.org/esmpy_doc/release/latest/ESMPy.pdf

    x_s: start longitude
    x_e: end longitude'
    x_i: lon incriment

    y_s: start latitude
    y_e: end latitude'
    y_i: lat incriment

    To perform regridding from Curvilinear data to rectilinear data we suggest to provide 
    Curvilinear as ds and rectilinear as ds_out
    '''
    if ds_out==None:

        

        if x_s==None and x_e==None and y_s==None and y_e==None:
            x_s=0
            x_e=360
            y_s=90
            y_e=-90
        if x_i==None:
            x_i=1
        if y_i==None:
            y_i=-1

        if isinstance(ds, xr.Dataset):
            ds_out = xr.Dataset(
            {
                "lat": (["lat"], np.arange(y_s, y_e+y_i, y_i)),
                "lon": (["lon"], np.arange(x_s, x_e+x_i, x_i)),
            }
            )

        elif isinstance(ds, xr.DataArray):
            ds_out = xr.DataArray(
            coords=[np.arange(y_s, y_e+y_i, y_i), np.arange(x_s, x_e+x_i, x_i)],
            dims=["lat", "lon"],
            )

        else:
            raise TypeError("Both ds should be either xarray.DataArray or xarray.Dataset.")

    if to_range is None:
        to_range = '0_360'
    if method is None:
        method = 'bilinear'
    
    regridder = xe.Regridder(ds, ds_out, method=method)


    if isinstance(ds, xr.DataArray) and isinstance(ds_out, xr.DataArray):

        regridded = regridder(ds)
    elif isinstance(ds, xr.Dataset) and isinstance(ds_out, xr.Dataset):

        # if var is None:
        #     raise ValueError("Please specify 'var' when regridding a Dataset.")
        regridded = regridder(ds)#[var])
    else:
        raise TypeError("Both ds and ds_out should be either xarray.DataArray or xarray.Dataset.")
    

    return adjust_longitude(rename_dims_to_standard(regridded), to_range=to_range, lon_name='lon')




