# anomaly.py
import xarray as xr
import numpy as np
import xeofs
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point#(data, coord=None, axis=-1) 


def compute_weights(data, lat_dim=None):
    """
    Compute weights based on the cosine of latitude values.

    Parameters:
    data (xarray.DataArray or xarray.Dataset): The input data containing latitude values.
    lat_dim (str, optional): The name of the latitude dimension in the data. Defaults to 'lat'.

    Returns:
    xarray.DataArray: Weights computed as the cosine of the latitude values in radians.
    """
    if lat_dim==None:
        lat_dim='lat'
    return np.cos(np.deg2rad(data[f'{lat_dim}']))

def calculate_anomaly(data, clim_start=None, climatology_dim='time', clim_end=None, freq='month'):   

    """
    Calculate anomalies by subtracting the climatology from the data.

    Parameters:
    data (xarray.DataArray or xarray.Dataset): The input data from which to calculate anomalies.
    clim_start (str, optional): The start year for the climatology period in 'YYYY' format. If None, the entire period is used.
    climatology_dim (str, optional): The dimension over which to calculate the climatology. Default is 'time'.
    clim_end (str, optional): The end year for the climatology period in 'YYYY' format. If None, the entire period is used.
    freq (str, optional): The frequency for grouping the data. Must be either 'month' or 'dayofyear'. Default is 'month'.

    Returns:
    xarray.DataArray or xarray.Dataset: The anomalies calculated by subtracting the climatology from the data.

    Raises:
    ValueError: If the frequency is not 'month' or 'dayofyear'.
    """

    if clim_start is None:
        if freq == 'month':
            return data.groupby(f'{climatology_dim}.{freq}') - data.groupby(f'{climatology_dim}.{freq}').mean((f'{climatology_dim}'))
        elif freq == 'dayofyear':
            return data.groupby(f'{climatology_dim}.{freq}') - data.groupby(f'{climatology_dim}.{freq}').mean((f'{climatology_dim}'))
        else:
            raise ValueError('Frequency must be "month" or "dayofyear".')
    else:
        climatology = data.sel(time=slice(f'{clim_start}-01-01', f'{clim_end}-12-31')).groupby(f'{climatology_dim}.{freq}').mean((f'{climatology_dim}'))
        return data.groupby(f'{climatology_dim}.{freq}') - climatology



def line_plot(data, figsize=None, dpi=None, variance_fraction=None, color=None, label=None):
    """
    Plots a line graph for the given data.

    Parameters:
    data (xarray.DataArray): The data to be plotted. Must be 1-dimensional and contain a 'time' dimension.
    figsize (tuple, optional): The size of the figure in inches (width, height). Defaults to None.
    dpi (int, optional): The resolution of the figure in dots per inch. Defaults to None.
    variance_fraction (float, optional): A variance fraction value to be displayed on the plot. Defaults to None.
    color (str, optional): The color of the line plot. Defaults to None.
    label (str, optional): The label for the plot. Defaults to None.

    Returns:
    None

    Raises:
    Exception: If an error occurs during plotting, it prints an error message.
    """


    try:
        if data.ndim == 1 and 'time' in data.dims:
            plt.figure(figsize=figsize, dpi=dpi)
            ax = plt.axes()
            if ax==None:
                plt.figure(figsize=(10, 3), dpi=300)
                ax=plt.axes()
            if color==None:
                color='k'   
            data.plot(ax=ax, color=color, lw=1, label=label)
            if variance_fraction is not None:
                y_position = data.max() - (data.max() * 0.05) 
                ax.text(int(str(data.time.data[0])[:4]), y_position, f'{label}_vf: {"%.2f" %variance_fraction}')
            # ax.set_title(f'{label}', loc=title_loc, color=color)
            ax.set_title('', loc='center', color='w')
            ax.legend(frameon=False)
            plt.show()
    except Exception as e:
        return print(f"Error while plotting: {e}")



def contour_plot(data, projection=None, figsize=None, dpi=None, cmap=None, extend=None, levels=None, central_lon=None, central_lat=None, ax_global=False):
    """
    Generate a contour plot for the given data.
    Parameters:
    data (xarray.DataArray): The data to be plotted. Must be a 2D array with 'lat' and 'lon' dimensions.
    projection (cartopy.crs.Projection, optional): The map projection to use. Defaults to PlateCarree with central_longitude.
    figsize (tuple, optional): The size of the figure in inches (width, height). Defaults to None.
    dpi (int, optional): The resolution of the figure in dots per inch. Defaults to None.
    cmap (str or matplotlib.colors.Colormap, optional): The colormap to use for the plot. Defaults to None.
    extend (str, optional): Whether to extend the colorbar at the ends. Options are 'neither', 'both', 'min', 'max'. Defaults to None.
    levels (list, optional): The contour levels to use. Defaults to 10 levels between the min and max of the data.
    central_lon (float, optional): The central longitude for the projection. Defaults to 0.
    central_lat (float, optional): The central latitude for the projection. Defaults to 0.
    ax_global (bool, optional): Whether to set the axis to global. Defaults to False.
    Returns:
    None
    """


    try:
        if data.ndim==2 and 'lat' in data.dims and 'lon' in data.dims:
            if central_lon==None:
                central_lon=0
            if central_lat==None:
                central_lat=0
            if projection==None:
                projection=ccrs.PlateCarree(central_longitude=central_lon)
            plt.figure(figsize=figsize, dpi=dpi)
            ax = plt.axes(projection=projection)
            lon=data.lon
            if levels == None:
                levels=list(np.linspace(data.min(), data.max(), 10))
            if (lon.min() <= -178 and lon.max() >= 178) or (lon.min() <= 2. and lon.max() >= 357.):
                cyclic_data, cyclic_lon = add_cyclic_point(data, coord=lon)

                cyclic_data = xr.DataArray(
                    cyclic_data, 
                    dims=data.dims,  # Keep the same dimensions
                    coords={**data.coords, 'lon': cyclic_lon},  # Replace the original longitude with cyclic longitude
                    attrs=data.attrs  # Copy the original attributes
                )
                if ax_global==True:
                    ax.set_global()
                 
                data = cyclic_data#.plot.contourf(levels=levels, cmap=cmap, extend=extend, transform=ccrs.PlateCarree())
            # else:
            data.plot.contourf(levels=levels, cmap=cmap, extend=extend, transform=ccrs.PlateCarree())
            # ax.coastlines()
            # ax.cfeature()
            ax.add_feature(cfeature.LAND, facecolor='grey')
            ax.add_feature(cfeature.OCEAN, facecolor='w')
            ax.add_feature(cfeature.COASTLINE)
    except Exception as e:
        return print(f"Error while plotting: {e}")



def compute_rotated_eofs(data, rotated=None, n_modes=None, standardize=None, use_coslat=None):
    """
    Compute EOFs using the xeofs module, with optional Varimax or Promax rotation.

    Parameters:
    -----------
    data : xarray.DataArray
        Input data with a time dimension.
    rotated : str, optional
        Specify 'Varimax' for orthogonal rotation or 'Promax' for oblique rotation.
        Leave as None for unrotated EOFs.
    n_modes : int, default=10
        Number of modes to compute.
    standardize : bool, optional
        Whether to standardize the data. Default is False.
    use_coslat : bool, optional
        If True (default), weights EOFs by the cosine of latitude for area-averaging.

    Returns:
    --------
    model : xeofs.single.EOF or xeofs.single.EOFRotator
        The fitted EOF model, either rotated or unrotated.

    Notes:
    ------
    - Varimax corresponds to orthogonal rotations (power=1).
    - Promax corresponds to oblique rotations (power=4).
    - Returns None if an invalid rotation option is provided.
    """
    if rotated==None:
        n_modes = n_modes if n_modes is not None else 1
    else:
        n_modes = n_modes if n_modes is not None else 10
    standardize = standardize if standardize is not None else False
    use_coslat = use_coslat if use_coslat is not None else True
    rotated = rotated if rotated is not None else False

    model = xeofs.single.EOF(n_modes=n_modes, standardize=standardize, use_coslat=use_coslat)
    
    try:
        model.fit(data, dim="time")
        
        # If no rotation is specified, return the fitted EOF model.
        if not rotated:
            return model
        
        # Choose the rotation method based on the input.
        if rotated == 'Varimax':
            rot_model = xeofs.single.EOFRotator(n_modes=n_modes, power=1)  # Varimax: Orthogonal rotation
            return rot_model.fit(model)
        elif rotated == 'Promax':
            rot_model = xeofs.single.EOFRotator(n_modes=n_modes, power=4)  # Promax: Oblique rotation
            return rot_model.fit(model)
        else:
            print("Invalid rotation option. Please specify None, 'Varimax', or 'Promax'.")
            return None
    
    except Exception as e:
        print(f"Error during EOF calculation: {e}")
        return None



def lanczos_filter_xarray(data, dT=1, Cf=None, Cf2=None, M=100, filter_type='low', time_dim=None):
    """
    Apply a Lanczos filter to an xarray DataArray using FFT-based filtering.
    
    Parameters:
    - data (xarray.DataArray): Input data to filter
    - dT (float): Sampling interval (default: 1)
    - Cf (float): Lower cut-off frequency in 1/dT units (default: Nyquist/2 for low/high-pass)
    - Cf2 (float): Upper cut-off frequency (only used for bandpass)
    - M (int): Number of coefficients (default: 100)
    - filter_type (str): Type of filter - 'low', 'high', or 'band'
    - time_dim (str): The name of the time dimension (default: auto-detect)
    
    Returns:
    - xarray.DataArray: Filtered data
    """
    # Auto-detect time dimension if not provided
    if time_dim is None:
        time_dim = [dim for dim in data.dims if "time" in dim.lower()]
        if not time_dim:
            raise ValueError("Time dimension not found. Please specify 'time_dim'.")
        time_dim = time_dim[0]
    

    Nf = 1 / (2 * dT)
    if Cf is None:
        Cf = Nf / 2
    
    Cf /= Nf
    
    if filter_type == 'band':
        if Cf2 is None:
            raise ValueError("For bandpass, Cf2 must be specified.")
        Cf2 /= Nf


    n = np.arange(0, M + 1)
    sigma = np.sinc(n / M)
    hk_low = Cf * np.sinc(2 * Cf * n) * sigma
    hk_high = -Cf * np.sinc(2 * Cf * n) * sigma
    hk_high[0] += 1
    
    if filter_type == 'low':
        coef = hk_low
    elif filter_type == 'high':
        coef = hk_high
    elif filter_type == 'band':
        hk_band = (Cf2 * np.sinc(2 * Cf2 * n) - Cf * np.sinc(2 * Cf * n)) * sigma
        coef = hk_band
    else:
        raise ValueError("Invalid filter type. Choose 'low', 'high', or 'band'")
    

    Ff = np.linspace(0, 1, data.sizes[time_dim])
    window = np.zeros_like(Ff)
    for i, f in enumerate(Ff):
        window[i] = coef[0] + 2 * np.sum(coef[1:] * np.cos(np.pi * np.arange(1, M + 1) * f))
    

    def apply_fft_filtering(arr):
        Cx = np.fft.rfft(arr)
        CxH = Cx * window[:len(Cx)]
        return np.fft.irfft(CxH, n=len(arr))
    
    filtered = xr.apply_ufunc(
        apply_fft_filtering,
        data,
        input_core_dims=[[time_dim]],
        output_core_dims=[[time_dim]],
        vectorize=True,
        dask="parallelized",
        output_dtypes=[data.dtype]
    )
    
    return filtered



def standardize_data(data, data_std_dev=None, dim=None):
    """
    Standardizes the input data along a specified dimension.

    Parameters:
    data (xarray.DataArray or numpy.ndarray): The input data to be standardized.
    data_std_dev (xarray.DataArray, numpy.ndarray, or None, optional): The standard deviation to use for standardization. 
        If None, the standard deviation of the input data along the specified dimension will be used. Default is None.
    dim (str or None, optional): The dimension along which to standardize the data. 
        If None, the default dimension 'time' will be used. Default is None.

    Returns:
    xarray.DataArray or numpy.ndarray: The standardized data.
    """


    if dim==None:
        dim='time'

    if data_std_dev==None:
        return data/data.std(dim=dim)
    else:
        return data/data_std_dev


def project_data_onto_eofs(data, eof_modes):
    """
    Projects the input data onto the provided Empirical Orthogonal Functions (EOF) modes.

    Parameters:
    data (xarray.DataArray): The input data to be projected.
    eof_modes (xarray.DataArray): The EOF modes onto which the data will be projected.

    Returns:
    xarray.DataArray: The projected data.
    """
    return xr.dot(data, eof_modes)

def stack_vars(list_vars, stack_name=None, drop_dims=[]):
    """
    Stack a list of xarray DataArray or Dataset objects along a new dimension.

    Parameters:
    -----------
    list_vars : list of xarray.DataArray or xarray.Dataset
        List of variables to be stacked.
    stack_name : str, optional
        Name of the new dimension along which to stack the variables. Default is 'variable'.
    drop_dims : list of str, optional
        List of dimension names to be dropped from each variable before stacking. Default is an empty list.

    Returns:
    --------
    xarray.DataArray or xarray.Dataset
        The stacked xarray object with the new dimension.
    """
    if stack_name==None:
        stack_name='variable'
    if len(drop_dims)>0:
        list_vars=[var.drop_vars(drop_dims, errors='ignore') for var in list_vars]
    return xr.concat(list_vars, dim='variable', coords='minimal', compat='override')