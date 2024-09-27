# eof_calculations.py

import numpy as np
from .utils import calculate_anomaly, compute_weights, compute_eofs



def calculate_global_mean_sst(data, lat_name='lat', lon_name='lon'):
    return calculate_anomaly(data).weighted(compute_weights(data, lat_dim='lat')).mean(dim=[lat_name, lon_name])



def global_sst_trend_and_enso(data, clim_start, clim_end, desired=None):
    '''This function calculates global sst warming trend, global sst warming pattern
        ENSO index, ENSO pattern and their corrosponding variance fraction.
        They are calculated as First (warming pattern and trend) and Second (ENSO 
        pattern and ENSO index) EOF modes of SST anomaly after removing
        the Annualcycle climatology.

        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose

        clim_start: climatology start year
        clim_end: climatology end year 
        desired: desired variables, can be choosen from 
        ['sst_trend_pattern', 'sst_trend_timeseries', 'variance_fraction_trend', 
        'enso_pattern', 'enso_index', 'variance_fraction_enso']'''
    
    if desired is None:

        desired = ['sst_trend_pattern', 'sst_trend_timeseries', 'variance_fraction_trend','enso_pattern', 'enso_index', 'variance_fraction_enso']
    

    data = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    
    solver=compute_eofs(data, lat_dim='lat')
    return_desired = []
    if 'sst_trend_pattern' in desired:
        return_desired.append(solver.eofs(neofs=2, eofscaling=2)[0])
    if 'sst_trend_timeseries' in desired:
        return_desired.append(solver.pcs(npcs=2, pcscaling=1)[:, 0])
    if 'enso_pattern' in desired:
        return_desired.append(solver.eofs(neofs=2, eofscaling=2)[1])
    if 'enso_index' in desired:
        return_desired.append(solver.pcs(npcs=2, pcscaling=1)[:, 1])
    if 'variance_fraction_trend' in desired:
        return_desired.append(solver.varianceFraction(neigs=2)[0])
    if 'variance_fraction_enso' in desired:
        return_desired.append(solver.varianceFraction(neigs=2)[1])
    
    return return_desired

def compute_pdo(data, clim_start, clim_end, desired=None):

    ''' This function calculates conventional PDO index and PDO pattern and 
        variance fraction.
        It is calculated as First EOF modes of SST anomaly in North Pacific above 20N 
        after removing the Annualcycle climatology and global mean SST (warming trend).

        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose

        clim_start: climatology start year
        clim_end: climatology end year 
        desired: desired variables, can be choosen from 
        ['pdo_pattern', 'pdo_index', 'variance_fraction_pdo'] '''

    if desired is None:
        desired = ['pdo_pattern', 'pdo_index', 'variance_fraction_pdo']
    data_anomaly = calculate_anomaly(data)
    data_pdo = data.sel(lat=slice(70, 20), lon=slice(110, 260))
    data_pdo_anomaly = calculate_anomaly(data_pdo, clim_start=clim_start, clim_end=clim_end) - calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
    solver=compute_eofs(data_pdo_anomaly, lat_dim='lat')
    return_desired = []
    if 'pdo_pattern' in desired:
        return_desired.append(solver.eofs(neofs=1, eofscaling=2).squeeze())
    if 'pdo_index' in desired:
        return_desired.append(solver.pcs(npcs=1, pcscaling=1).squeeze())
    if 'variance_fraction_pdo' in desired:
        return_desired.append(solver.varianceFraction(neigs=1))

    return return_desired




def compute_amo(data, clim_start, clim_end, smoothing_window=None, desired=None):

    ''' This function calculates conventional AMO index and AMO pattern.
        It is calculated as area-averaged SST anomalies and time averaged 
        SST anomalies in North Atlantic above 0N after removing the Annualcycle 
        climatology and global mean SST (warming trend).

        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose

        clim_start: climatology start year
        clim_end: climatology end year 
        smoothing_window: (optional) time period for running mean
        desired: desired variables, can be choosen from 
        ['amo_pattern', 'amo_index'] '''

    if desired==None:
        desired = ['amo_pattern', 'amo_index']
    north_atlantic_sst = data.sel(lat=slice(60, 0), lon=slice(280, 360))
    

    data_anomalies = calculate_anomaly(north_atlantic_sst, clim_start=clim_start, clim_end=clim_end)
    

    global_mean_data = calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
    

    regional_anomaly = data_anomalies - global_mean_data
    

    if smoothing_window!=None:
        regional_anomaly = regional_anomaly.rolling(time=smoothing_window, center=True).mean()
    

    amo_index = regional_anomaly.mean(('lat', 'lon'))
    amo_pattern = regional_anomaly.mean(('time'))
    return_desired = []
    if 'amo_pattern' in desired:
        return_desired.append(amo_pattern)
    if 'amo_index' in desired:
        return_desired.append(amo_index)
    
    return return_desired

