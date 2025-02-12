#preprocess_data.py

import xarray as xr
import xesmf as xe
import numpy as np


def rename_dims_to_standard(ds):
    """
    Rename the dimensions of an xarray Dataset to standard names ('lon', 'lat', 'time') based on their units.
    Parameters:
    ds (xarray.Dataset): The input dataset with dimensions to be renamed.
    Returns:
    xarray.Dataset: The dataset with renamed dimensions if applicable.
    The function performs the following steps:
    1. Detects the longitude dimension by checking for the unit 'degrees_east'.
    2. Detects the latitude dimension by checking for the unit 'degrees_north'.
    3. Detects the time dimension by checking for units like 'days since', 'seconds since', or 'months since'.
    4. Renames the detected dimensions to 'lon', 'lat', and 'time' respectively.
    """

    
    rename_dict = {}

    # Step 1: Detect longitude
    if 'lon' not in ds.dims:
        for coord in ds.coords:
            if 'degrees_east' in ds.coords[coord].attrs.get('units', ''):
                rename_dict[coord] = 'lon'
                break

    # Step 2: Detect latitude
    if 'lat' not in ds.dims:
        for coord in ds.coords:
            if 'degrees_north' in ds.coords[coord].attrs.get('units', ''):
                rename_dict[coord] = 'lat'
                break

    # Step 3: Detect time
    if 'time' not in ds.dims:
        for coord in ds.coords:
            if 'days since' in ds.coords[coord].attrs.get('units', '') or 'seconds since' in ds.coords[coord].attrs.get('units', '') \
            or 'months since' in ds.coords[coord].attrs.get('units', ''):
                rename_dict[coord] = 'time'
                break

    # Step 4: Rename the detected dimensions
    if rename_dict:
        ds = ds.rename(rename_dict)
    
    return ds


def adjust_latitude(ds, lat_name='lat'):
    """
    Adjusts the latitude coordinates of an xarray Dataset to be in descending order.

    Parameters:
    ds (xarray.Dataset): The input dataset containing latitude coordinates.
    lat_name (str, optional): The name of the latitude coordinate in the dataset. Default is 'lat'.

    Returns:
    xarray.Dataset: The dataset with latitude coordinates sorted in descending order.
    """

    return ds.sortby(lat_name, ascending=False)


def adjust_longitude(ds, lon_name='lon', to_range='0_360'):
    """
    Adjusts the longitude values in the given dataset to the specified range.
    Parameters:
    ds (xarray.Dataset): The input dataset containing longitude values.
    lon_name (str, optional): The name of the longitude variable in the dataset. Default is 'lon'.
    to_range (str, optional): The target range for longitude values. 
                              Can be '0_360' for [0, 360) or '-180_180' for [-180, 180). Default is '0_360'.
    Returns:
    xarray.Dataset: The dataset with adjusted longitude values.
    Raises:
    ValueError: If the specified target range is not '0_360' or '-180_180'.
    """
    

    
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
    

    ds = rename_dims_to_standard(xr.open_dataset(path))
    

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
    """
    Save the given data to a NetCDF file.

    Parameters:
    data (xarray.Dataset or xarray.DataArray): The data to be saved.
    file_path (str): The path where the NetCDF file will be saved.

    Returns:
    None
    """

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
        if ds_out is None, regridding will be done using a generic grid made using xe, xs, ye, ys, xi, and yi.
        
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
    x_i: lon increment

    y_s: start latitude
    y_e: end latitude'
    y_i: lat increment

    To perform regridding from Curvilinear data to rectilinear data we suggest providing 
    Curvilinear as ds and rectilinear as ds_out.
    '''
    if ds_out is None:
        if x_s is None and x_e is None and y_s is None and y_e is None:
            x_s = 0
            x_e = 360
            y_s = 90
            y_e = -90
        if x_i is None:
            x_i = 1
        if y_i is None:
            y_i = -1

        if isinstance(ds, xr.Dataset):
            ds_out = xr.Dataset(
                {
                    "lat": (["lat"], np.arange(y_s, y_e + y_i, y_i)),
                    "lon": (["lon"], np.arange(x_s, x_e + x_i, x_i)),
                }
            )
        elif isinstance(ds, xr.DataArray):
            ds_out = xr.DataArray(
                coords=[np.arange(y_s, y_e + y_i, y_i), np.arange(x_s, x_e + x_i, x_i)],
                dims=["lat", "lon"],
            )
        else:
            raise TypeError("ds should be either xarray.DataArray or xarray.Dataset.")

    if to_range is None:
        to_range = '0_360'
    if method is None:
        method = 'bilinear'
    
    regridder = xe.Regridder(ds, ds_out, method=method)

    if isinstance(ds, xr.DataArray) and isinstance(ds_out, xr.DataArray):
        regridded = regridder(ds)
    elif isinstance(ds, xr.Dataset) and isinstance(ds_out, xr.Dataset):
        regridded = regridder(ds)
    else:
        raise TypeError("Both ds and ds_out should be either xarray.DataArray or xarray.Dataset.")
    
    return adjust_longitude(rename_dims_to_standard(regridded), to_range=to_range, lon_name='lon')
