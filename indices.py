# eof_calculations.py

import numpy as np
from .utils import calculate_anomaly, compute_weights, compute_eofs



def calculate_global_mean_sst(data, lat_name='lat', lon_name='lon'):
    return calculate_anomaly(data).weighted(compute_weights(data, lat_dim='lat')).mean(dim=[lat_name, lon_name])



def global_sst_trend_and_enso(data, clim_start=1981, clim_end=2010, desired=None):
    if desired is None:
        desired = ['sst_trend_pattern', 'sst_trend_timeseries', 'enso_pattern', 'enso_index', 'variance_fraction']
    

    data = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    
    solver=compute_eofs(data, lat_dim='lat')
    # Return requested values
    return_desired = []
    if 'sst_trend_pattern' in desired:
        return_desired.append(solver.eofs(neofs=2, eofscaling=2)[0])
    if 'sst_trend_timeseries' in desired:
        return_desired.append(solver.pcs(npcs=2, pcscaling=1)[:, 0])
    if 'enso_pattern' in desired:
        return_desired.append(solver.eofs(neofs=2, eofscaling=2)[1])
    if 'enso_index' in desired:
        return_desired.append(solver.pcs(npcs=2, pcscaling=1)[:, 1])
    if 'variance_fraction' in desired:
        return_desired.append(solver.varianceFraction(neigs=2))
    
    return return_desired

def compute_pdo(data, clim_start, clim_end, desired=None):
    if desired is None:
        desired = ['pdo_pattern', 'pdo_index', 'variance_fraction']
    data_anomaly = calculate_anomaly(data)
    data_pdo = data.sel(lat=slice(70, 20), lon=slice(110, 260))
    data_pdo_anomaly = calculate_anomaly(data_pdo, clim_start=clim_start, clim_end=clim_end) - calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
    solver=compute_eofs(data_pdo_anomaly, lat_dim='lat')
    return_desired = []
    if 'pdo_pattern' in desired:
        return_desired.append(solver.eofs(neofs=1, eofscaling=1).squeeze())
    if 'pdo_index' in desired:
        return_desired.append(solver.pcs(npcs=1, pcscaling=1).squeeze())
    if 'variance_fraction' in desired:
        return_desired.append(solver.varianceFraction(neigs=1))

    return return_desired




def compute_amo(data, clim_start=1981, clim_end=2010, smoothing_window=None, desired=None):
    if desired==None:
        desired = ['amo_pattern', 'amo_index']
    north_atlantic_sst = data.sel(lat=slice(60, 0), lon=slice(280, 360))
    

    data_anomalies = calculate_anomaly(north_atlantic_sst, clim_start=clim_start, clim_end=clim_end)
    

    global_mean_data = calculate_global_mean_sst(data)
    

    regional_anomaly = data_anomalies - global_mean_data
    

    if smoothing_window!=None:
        regional_anomaly = regional_anomaly.rolling(time=smoothing_window, center=True).mean()
    

    amo_index = regional_anomaly.mean(dim=['lat', 'lon'])
    amo_pattern = regional_anomaly.mean(dim=['time'])
    return_desired = []
    if desired=='amo_pattern':
        return_desired.append(amo_pattern)
    if desired=='amo_index':
        return_desired.append(amo_index)
    
    return return_desired

