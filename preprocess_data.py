#preprocess_data.py

import xarray as xr


def load_data(path, var, start_time=None, end_time=None, lat_s=None, lat_e=None, lon_s=None, lon_e=None):

	''' This function loads the variables from nc files as xarray.DataArray 
		path: directory to nc file
		var : variables to be extracted
		start_time: start time for the variables to be extracted
		end_time: end time for the variables to be extracted   
		(end_time - start_time = time period for analysis)
		lat_s: start latitude
		lat_e: end latitude (check latitude order using ncdump -v lat ncfile.nc 
		lat_s and lat_e should be choosen in earlier and later latidues, in the 
		output of ncdump, both should be provided or none for global)
		lon_s: start longitude
		lon_e: end longitude (check longitude order using ncdump -v lon ncfile.nc 
		lon_s and lon_e should be choosen in order of earlier and later longidues, 
		in the output of ncdump, both should be provided or none for global)
		'''
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
    """Save the given data to a NetCDF file.
    data: xarray.DataArray to be saved on netcdf format
    file_path: directory where file needs to be saved"""
    data.to_netcdf(file_path)
    print(f"Data saved to {file_path}")


