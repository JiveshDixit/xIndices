#preprocess_data.py

import xarray as xr


def load_data(path, var, start_time=None, end_time=None, lat_s=None, lat_e=None, lon_s=None, lon_e=None):
	if (start_time == None or end_time==None) and (lat_s==None or lat_e==None) and(lon_s==None or lon_e==None):
		return xr.open_dataset(path)[var]
	elif (lat_s==None or lat_e==None) and (lon_s==None or lon_e==None):
		return xr.open_dataset(path)[var].sel(time=slice(start_time, end_time))

	elif (start_time == None or end_time==None) and(lon_s==None or lon_e==None):
		return xr.open_dataset(path)[var].sel(lat=slice(lat_s, lat_e))

	elif (start_time == None or end_time==None) and(lat_s==None or lat_e==None):
		return xr.open_dataset(path)[var].sel(lon=slice(lon_s, lon_e))

	elif (start_time == None or end_time==None):
		return xr.open_dataset(path)[var].sel(lon=slice(lon_s, lon_e), lat=slice(lat_s, lat_e))
	elif (lat_s==None or lat_e==None):
		 return xr.open_dataset(path)[var].sel(lon=slice(lon_s, lon_e), time=slice(start_time, end_time))

	elif (lon_s==None or lon_e==None):
		return xr.open_dataset(path)[var].sel(lat=slice(lat_s, lat_e), time=slice(start_time, end_time))

	else:
		return xr.open_dataset(path)[var].sel(lat=slice(lat_s, lat_e), time=slice(start_time, end_time), lon=slice(lon_s, lon_e))


def write_netcdf(data, file_path):
    """Save the given data to a NetCDF file."""
    data.to_netcdf(file_path)
    print(f"Data saved to {file_path}")


