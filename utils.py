# anomaly.py

import xarray as xr
import numpy as np
from eofs.xarray import Eof
import xeofs
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.util import add_cyclic_point#(data, coord=None, axis=-1) 


def compute_weights(data, lat_dim=None):
    if lat_dim==None:
        lat_dim='lat'
    """Compute cosine weights based on latitude."""
    return np.cos(np.deg2rad(data[f'{lat_dim}']))

def calculate_anomaly(data, clim_start=None, climatology_dim='time', clim_end=None, freq='month'):   
    """Calculate anomaly based on climatology."""
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


def compute_eofs(data, lat_dim='lat'):

    ''' This functions computes EOF using eofs module '''

    coslat = np.cos(np.deg2rad(data.coords[lat_dim].values))
    weights = np.sqrt(coslat)

    if weights.ndim == 1 and len(weights) == data.sizes[lat_dim]:
        # Expand weights for broadcasting
        weights = weights[..., np.newaxis]  # Add a new axis for broadcasting in EOF calculation
    else:
        raise ValueError("Weights dimensions do not align with the data anomaly.")

    try:
        if lat_dim not in data.dims:
            solver = Eof(data)
        else:
            solver = Eof(data, weights=weights)
        return solver
        
    except Exception as e:
        print(f"Error creating EOF solver: {e}")
        return None  # Return None on failure to avoid confusion with the exception message

def line_plot(data, figsize=None, dpi=None, variance_fraction=None, color=None, label=None):

    ''' This function plots the calculated indices for the priliminary check 
        if the user wants.
        data: 1D data to be plot
        figsize: size of the canvas. Tuple e.g. (10, 3) default
        dpi : dots per inches-square. Integer 300 default
        variance_fraction: Variance fraction calculated from the given functions 
        such as in calculate_pdo etc.
        color: color for the line desired, black if None
        label: label for the line to be plotted, e.g. PDO, ENSO etc.'''
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



def contour_plot(data, projection=None, figsize=None, dpi=None, cmap=None, extend=None, levels=None, central_lon=None, central_lat=None):

    ''' This function plots the calculated variability patterbs for the 
        priliminary check if the user wants.
        data (xr_DataArray): 2D data to be plot
        projection (projection object ccrs.Projection_type()): cartopy projection for contour plot
        cmap (str): colormap
        extend (str): extend colorbar, takes arguments, max, min, both 
        figsize (tuple; e.g. default (12, 6)): size of the canvas.
        dpi (int default 450): dots per inches-square
        central_lat: center of latitude for projection
        central_lon: centre of longitude for projection
        levels (list sorted as min to max.)= contour levels

        '''

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
                ax.set_global()
                 
                data = cyclic_data#.plot.contourf(levels=levels, cmap=cmap, extend=extend, transform=ccrs.PlateCarree())
            # else:
            data.plot.contourf(levels=levels, cmap=cmap, extend=extend, transform=ccrs.PlateCarree())
            # ax.coastlines()
            # ax.cfeature()
            ax.add_feature(cfeature.LAND)
            ax.add_feature(cfeature.OCEAN)
            ax.add_feature(cfeature.COASTLINE)
    except Exception as e:
        return print(f"Error while plotting: {e}")



def compute_rotated_eofs(data, rotated=None, n_modes=10, standardize=None, use_coslat=None):
    ''' This functions computes EOF using eofs module 

        data: xarray.DataArray with time dimension
        rotated (str): Unrotated EOFs if None, otherwise 
        varimax for orthogonal rotations or Promax for Oblique
        use_coslat (boolean): True if None, otherwise give False. It is used to calculated area-averaged EOFs
        standardize (Boolean) = False if None, make it True if you want to standardize
        n_modes (int >0): change accordingly''' 

    if standardize==None:
        standardize=False
    if use_coslat==None:
        use_coslat=True

    if rotated == None:
        rotated=False
    model = xeofs.single.EOF(n_modes=n_modes, standardize=standardize, use_coslat=use_coslat)
    model.fit(data, dim="time")
    try:
        if rotated==False:
            return model

        if rotated == 'Varimax':
            rot_model = xeofs.single.EOFRotator(n_modes=n_modes, power=1)  ## power=1, 'Varimax (Orthogonal) rotation'
            return rot_model.fit(model)
        elif rotated == 'Promax':
            rot_model = xeofs.single.EOFRotator(n_modes=n_modes, power=4)  ## power=1, 'Promax (Obligue) rotation'
            return rot_model.fit(model)
        else:
            print('Incorrect statement for rotated, give only None or Varimax or Promax')        
        return None



    except Exception as e:
        print(f"Error creating EOF solver: {e}")
        return None  # Return None on failure to avoid confusion with the exception message
