# eof_calculations.py

import numpy as np
from .utils import calculate_anomaly, compute_weights, compute_eofs, compute_rotated_eofs
import xarray as xr



def calculate_global_mean_sst(data, lat_name='lat', lon_name='lon'):
    return calculate_anomaly(data).weighted(compute_weights(data)).mean(dim=[lat_name, lon_name])



def global_sst_trend_and_enso(data, clim_start=None, clim_end=None, desired=None):
    '''This function calculates global sst warming trend, global sst warming pattern
        ENSO index, ENSO pattern and their corrosponding variance fraction.
        They are calculated as First (warming pattern and trend) and Second (ENSO 
        pattern and ENSO index) EOF modes of SST anomaly after removing
        the Annualcycle climatology.

        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose

        clim_start: climatology start year
        clim_end: climatology end year (if both None, whole period will be chosen to compute climatology)
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
    if 'variance_fraction_trend' in desired:
        return_desired.append(solver.varianceFraction(neigs=2)[0])
    if 'enso_pattern' in desired:
        return_desired.append(solver.eofs(neofs=2, eofscaling=2)[1])
    if 'enso_index' in desired:
        return_desired.append(solver.pcs(npcs=2, pcscaling=1)[:, 1])
    if 'variance_fraction_enso' in desired:
        return_desired.append(solver.varianceFraction(neigs=2)[1])
    
    return return_desired

def compute_pdo(data, clim_start=None, clim_end=None, desired=None, lat_s=None, lat_e=None, lon_s=None, lon_e=None):

    if lat_s==None and lat_e==None and lon_s==None and lon_e==None:
        lat_s = 70
        lat_e = 20
        lon_s = 110
        lon_e = 260
    ''' This function calculates conventional PDO index and PDO pattern and 
        variance fraction.
        It is calculated as First EOF modes of SST anomaly in North Pacific above 20N 
        after removing the Annualcycle climatology and global mean SST (warming trend).

        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose

        clim_start: climatology start year
        clim_end: climatology end year (if both None, whole period will be chosen to compute climatology)
        desired: desired variables, can be choosen from 
        ['pdo_pattern', 'pdo_index', 'variance_fraction_pdo'] 
        lat_s = start latitude
        lat_e = end latitude
        lon_s = start longitude
        lon_e = end longitude'''

    if desired is None:
        desired = ['pdo_pattern', 'pdo_index', 'variance_fraction_pdo']
    data_anomaly = calculate_anomaly(data)
    data_pdo = data.sel(lat=slice(lat_s, lat_e), lon=slice(lon_s, lon_e))
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




def compute_amo(data, clim_start=None, clim_end=None, smoothing_window=None, desired=None, lat_s=None, lat_e=None, lon_s=None, lon_e=None):

    if lat_s==None and lat_e==None and lon_s==None and lon_e==None:
        lat_s = 70
        lat_e = 0
        lon_s = 280
        lon_e = 360
    ''' This function calculates conventional AMO index and AMO pattern.
        It is calculated as area-averaged SST anomalies and time averaged 
        SST anomalies in North Atlantic above 0N after removing the Annualcycle 
        climatology and global mean SST (warming trend).

        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose

        clim_start: climatology start year
        clim_end: climatology end year (if both None, whole period will be chosen to compute climatology)
        smoothing_window: (optional) time period for running mean
        desired: desired variables, can be choosen from 
        ['amo_pattern', 'amo_index'] 
        lat_s = start latitude
        lat_e = end latitude
        lon_s = start longitude
        lon_e = end longitude'''

    if desired==None:
        desired = ['amo_pattern', 'amo_index']
    north_atlantic_sst = data.sel(lat=slice(lat_s, lat_e), lon=slice(lon_s, lon_e))
    

    data_anomalies = calculate_anomaly(north_atlantic_sst, clim_start=clim_start, clim_end=clim_end)
    

    global_mean_data = calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
    

    amo_index = data_anomalies.weighted(compute_weights(data_anomalies)).mean(('lat', 'lon')) - global_mean_data
    

    if smoothing_window!=None:
        amo_index = amo_index.rolling(time=smoothing_window, center=True).mean().dropna(dim='time')
    

    # amo_index = regional_anomaly
    amo_pattern = xr.cov(calculate_anomaly(data), amo_index, dim='time')/amo_index.var()
    return_desired = []
    if 'amo_pattern' in desired:
        return_desired.append(amo_pattern)
    if 'amo_index' in desired:
        return_desired.append(amo_index)
    
    return return_desired


def compute_nao(data, clim_start=None, clim_end=None, desired=None, lat_s=None, lat_e=None, rotated=None, use_coslat=None, standardize=False, n_modes=2):

    ''' This function calculates NAO index, NAO pattern and variance fraction.
        It is calculated as Second EOF modes of 500mb Geo-potential height 
        anomaly above 20N after removing the Annualcycle climatology.

        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose

        clim_start: climatology start year
        clim_end: climatology end year (if both None, whole period will be chosen to compute climatology)
        desired: desired variables, can be choosen from 
        ['pdo_pattern', 'pdo_index', 'variance_fraction_pdo'] 
        lat_s = start latitude
        lat_e = end latitude
        rotated: if rotated analysis is required. None if unrotated, 
        Varimax and Promax for rotated
        use_coslat: True if None, otherwise give False. It is used to calculated area-averaged EOFs
        standardize = False if None, make it True if you want to standardize
        n_modes: default 2; this will assume that 2nd mode is NAO, change accordingly'''


    if desired is None:

        desired = ['nao_pattern', 'nao_index', 'variance_fraction_nao']



    north_geop = data.sel(lat=slice(lat_s, lat_e))
    

    data_anomalies = calculate_anomaly(north_geop, clim_start=clim_start, clim_end=clim_end)
    

    nao_index = compute_rotated_eofs(data_anomalies, rotated=rotated, n_modes=n_modes, standardize=standardize, use_coslat=use_coslat).scores()[n_modes-1]

    nao_index = nao_index/nao_index.std()
    
    nao_pattern = compute_rotated_eofs(data_anomalies, rotated=rotated, n_modes=n_modes, standardize=standardize, use_coslat=use_coslat).components()[n_modes-1]

    variance_fraction_nao = compute_rotated_eofs(data_anomalies, rotated=rotated, n_modes=n_modes, standardize=standardize, use_coslat=use_coslat).explained_variance_ratio()[1]
    return_desired = []
    if 'nao_pattern' in desired:
        return_desired.append(nao_pattern)
    if 'nao_index' in desired:
        return_desired.append(nao_index)
    if 'variance_fraction_nao' in desired:
        return_desired.append(variance_fraction_nao)
    
    return return_desired     