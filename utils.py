# anomaly.py

import xarray as xr
import numpy as np
from eofs.xarray import Eof
import xeofs
import matplotlib.pyplot as plt


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

def line_plot(data, variance_fraction=None, color=None, label=None, ax=None):

    ''' This function plots the calculated indices for the priliminary check 
        if the user wants.
        data: 1D data to be plot
        variance_fraction: Variance fraction calculated from the given functions 
        such as in calculate_pdo etc.
        color: color for the line desired, black if None
        label: label for the line to be plotted, e.g. PDO, ENSO etc.'''
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


def compute_rotated_eofs(data, rotated=None, n_modes=10, standardize=None, use_coslat=None):
    ''' This functions computes EOF using eofs module 

        data: xarray.DataArray with time dimension
        rotated: Unrotated EOFs if None, , otherwise 
        varimax for orthogonal rotations or Promax for Oblique
        use_coslat: True if None, otherwise give False. It is used to calculated area-averaged EOFs
        standardize = False if None, make it True if you want to standardize
        n_modes: default 2; this will assume that 2nd mode is NAO, change accordingly''' 

    if standardize==None:
        standardize=False
    if use_coslat==None:
        use_coslat=True


    model = xeofs.single.EOF(n_modes=n_modes, standardize=standardize, use_coslat=use_coslat)
    model.fit(data, dim="time")
    try:
        if rotated==None:
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