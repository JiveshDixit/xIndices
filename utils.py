# anomaly.py

import xarray as xr
import numpy as np
from eofs.xarray import Eof

def compute_weights(data, lat_dim='lat'):
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

    if lat_dim not in data.dims:
        raise ValueError(f"Latitude dimension '{lat_dim}' not found in data.")

    coslat = np.cos(np.deg2rad(data.coords[lat_dim].values))
    weights = np.sqrt(coslat)

    if weights.ndim == 1 and len(weights) == data.sizes[lat_dim]:
        # Expand weights for broadcasting
        weights = weights[..., np.newaxis]  # Add a new axis for broadcasting in EOF calculation
    else:
        raise ValueError("Weights dimensions do not align with the data anomaly.")

    try:
        solver = Eof(data, weights=weights)
        return solver
        
    except Exception as e:
        print(f"Error creating EOF solver: {e}")
        return None  # Return None on failure to avoid confusion with the exception message

