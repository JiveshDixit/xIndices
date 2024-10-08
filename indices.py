# eof_calculations.py

import numpy as np
from .utils import calculate_anomaly, compute_weights, compute_eofs, compute_rotated_eofs
import xarray as xr
from .preprocess_data import load_data, rename_dims_to_standard, adjust_longitude



def calculate_global_mean_sst(data, lat_name='lat', lon_name='lon'):
    return calculate_anomaly(data).weighted(compute_weights(data)).mean(dim=[lat_name, lon_name])



def global_sst_trend_and_enso(data=None, path=None, var=None ,clim_start=None, clim_end=None, desired=None, start_time=None, end_time=None, to_range=None, standardize=None, normalize_pattern=None, normalize_index=None):
    '''This function calculates global sst warming trend, global sst warming pattern
        ENSO index, ENSO pattern and their corrosponding variance fraction.
        They are calculated as First (warming pattern and trend) and Second (ENSO 
        pattern and ENSO index) EOF modes of SST anomaly after removing
        the Annualcycle climatology.

        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose
        path (directory): path to data
        var (str): variable name
        clim_start: climatology start year
        clim_end: climatology end year (if both None, whole period will be chosen to compute climatology)
        desired: desired variables, can be choosen from 
        ['sst_trend_pattern', 'sst_trend_timeseries', 'variance_fraction_trend', 
        'enso_pattern', 'enso_index', 'variance_fraction_enso']
        start_time (int): start year for the data to be visulaized
        end_time (int): end year for the data to be visulaized
        to_range (str default 0_360): Range of longitude for the data, 0_360 or -180_180
        standardize (boolean): Normalize the data with Standard Deviation
        Normalize_pattern (boolean): Normalize components (spatial Pattern) with singular values
        Normalize_index (boolean): Normalize scores (timeseries) with singular values'''    
    
    if desired is None:
        desired = ['sst_trend_pattern', 'sst_trend_timeseries', 'variance_fraction_trend','enso_pattern', 'enso_index', 'variance_fraction_enso']
    if standardize==None:
        standardize=False
    if normalize_index==None:
        normalize_index = False
    if normalize_pattern==None:
        normalize_pattern = True
    
    if to_range==None:
        to_range='0_360'    
    if path is not None and var is not None:
        if to_range==None:
            to_range='0_360' ## otherwise provide -180_180
        data = adjust_longitude(rename_dims_to_standard(load_data(path, var, start_time=start_time, end_time=end_time)), to_range=to_range)
        data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    elif data is not None:
        data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    solver = compute_rotated_eofs(data, rotated=False, n_modes=2, standardize=None, use_coslat=True)
    # solver=compute_eofs(data_anom, lat_dim='lat')
    return_desired = []
    # eofs_ = solver.eofs(neofs=2, eofscaling=2)
    # pcs_  = solver.pcs(npcs=2, pcscaling=1)
    eofs_ = solver.components(normalized=normalize_pattern)
    pcs_ = solver.scores(normalized=normalize_index)
    var_frac_ = solver.explained_variance_ratio()
    # var_frac_ = solver.varianceFraction(neigs=2)
    if 'sst_trend_pattern' in desired:
        return_desired.append(eofs_[0].squeeze())
    if 'sst_trend_timeseries' in desired:
        return_desired.append(pcs_[0].squeeze())
    if 'variance_fraction_trend' in desired:
        return_desired.append(var_frac_[0].squeeze())
    if 'enso_pattern' in desired:
        return_desired.append(eofs_[1].squeeze())
    if 'enso_index' in desired:
        return_desired.append(pcs_[1].squeeze())
    if 'variance_fraction_enso' in desired:
        return_desired.append(var_frac_[1].squeeze())

    
    if len(return_desired)==1:
        return return_desired[0]
    else:
        return return_desired



def compute_regional_eof_modes(data=None, path=None, var=None ,clim_start=None, clim_end=None, desired=None, start_time=None, end_time=None, 
    lat_s=None, lat_e=None, lon_s=None, lon_e=None, to_range=None, n_modes=None, remove_trend=None, rotated=None, use_coslat=None, standardize=None, 
    normalize_pattern=None, normalize_index=None):
    '''This function is more generalized form of global_sst_trend_and_enso function.
        
        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose
        path (directory): path to data
        var (str): variable name
        desired: desired variables, can be choosen from 
        ['regional_patterns', 'regional_timeseries', 'variance_fractions_regional']
        start_time (int): start year for the data to be visulaized
        end_time (int): end year for the data to be visulaized
        to_range (str default 0_360): Range of longitude for the data, 0_360 or -180_180
        lat_s = start latitude
        lat_e = end latitude
        lon_s = start longitude
        lon_e = end longitude
        standardize (boolean): Normalize the data with Standard Deviation
        Normalize_pattern (boolean): Normalize components (spatial Pattern) with singular values
        Normalize_index (boolean): Normalize scores (timeseries) with singular values
        n_modes (int): number of modes to be calculated
        remove_trend (boolean): Remove global mean variable (a timeseries)
        rotated (str): Unrotated EOFs if None, otherwise 
        Varimax for orthogonal rotations or Promax for Oblique
        use_coslat (boolean): True if None, otherwise give False. It is used to calculated area-averaged EOFs
        clim_start (int): Climatology start year
        clim_end (int): Climatology end year  (if both None, whole period will be chosen to compute climatology)
'''

    if lat_s==None and lat_e==None and lon_s==None and lon_e==None:
        lat_s = 90
        lat_e = -90
        lon_s = 0
        lon_e = 360

    if rotated ==None:
        rotated = False

    if standardize==None:
        standardize=False

    if use_coslat==None:
        use_coslat=True

    if normalize_index==None:
        normalize_index = False
    if normalize_pattern==None:
        normalize_pattern = True
    
    if remove_trend==None:
        remove_trend==False    
    
    if desired is None:
  
        desired = ['regional_patterns', 'regional_timeseries', 'variance_fractions_regional']

    if to_range==None:
        to_range='0_360'    
    if path is not None and var is not None:
        if to_range==None:
            to_range='0_360' ## otherwise provide -180_180
        data = adjust_longitude(rename_dims_to_standard(load_data(path, var, start_time=start_time, end_time=end_time, lat_s=lat_s, lat_e=lat_e, lon_s=lon_s, lon_e=lon_e)), to_range=to_range)
        # data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    elif data is not None:
        data = data
    if remove_trend==False:

        data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    else:
        data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end) - calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
    solver = compute_rotated_eofs(data, rotated=rotated, n_modes=n_modes, standardize=standardize, use_coslat=use_coslat)
    # solver=compute_eofs(data_anom, lat_dim='lat')
    return_desired = []
    if 'regional_patterns' in desired:
        return_desired.append(solver.components(normalized=normalize_pattern).squeeze())
    if 'regional_timeseries' in desired:
        return_desired.append(solver.scores(normalized=normalize_index).squeeze())
    if 'variance_fractions_regional' in desired:
        return_desired.append(solver.explained_variance_ratio().squeeze())

    if len(return_desired)==1:
        return return_desired[0]
    else:
        return return_desired




def compute_pdo(data=None, path=None, var=None ,clim_start=None, clim_end=None, desired=None, start_time=None, end_time=None, to_range=None, 
    standardize=None, normalize_pattern=None, normalize_index=None, lat_s=None, lat_e=None, lon_s=None, lon_e=None, remove_trend=None):

    ''' This function calculates conventional PDO index and PDO pattern and 
        variance fraction.
        It is calculated as First EOF modes of SST anomaly in North Pacific above 20N 
        after removing the Annualcycle climatology and global mean SST (warming trend).

        data: Processed gridded SST data in the shape of (time, lat, lon)
        if not in the order, can be reordered as xarray.transpose
        path (directory): path to data
        var (str): variable name
        clim_start: climatology start year
        clim_end: climatology end year (if both None, whole period will be chosen to compute climatology)
        desired: desired variables, can be choosen from 
        ['pdo_pattern', 'pdo_index', 'variance_fraction_pdo'] 
        start_time (int): start year for the data to be visulaized
        end_time (int): end year for the data to be visulaized
        to_range (str default 0_360): Range of longitude for the data, 0_360 or -180_180
        standardize (boolean): Normalize the data with Standard Deviation
        Normalize_pattern (boolean): Normalize components (spatial Pattern) with singular values
        Normalize_index (boolean): Normalize scores (timeseries) with singular values
        remove_trend (boolean): default is False and PDO index is mode 2, otherwise mode 1.

        lat_s = start latitude
        lat_e = end latitude
        lon_s = start longitude
        lon_e = end longitude
        latitude and longitude ranges can be choosen to experience various versions of PDO'''
    n_modes=None

    if lat_s==None and lat_e==None and lon_s==None and lon_e==None:
        lat_s = 70
        lat_e = 20
        lon_s = 110
        lon_e = 260
    if remove_trend==None or remove_trend==False:
        remove_trend==False
        n_modes=2
    elif remove_trend==True:
        n_modes=1
    else:
        print('remove_trends takes only boolean arguments, i.e. True or False')
    if standardize==None:
        standardize=False
    if normalize_index==None:
        normalize_index = False
    if normalize_pattern==None:
        normalize_pattern = True
    if to_range==None:
        to_range='0_360'    ## otherwise provide -180_180


    if desired is None:
        desired = ['pdo_pattern', 'pdo_index', 'variance_fraction_pdo']

    if path is not None and var is not None:

        data = adjust_longitude(rename_dims_to_standard(load_data(path, var, start_time=start_time, end_time=end_time, lat_s=lat_s, lat_e=lat_e, lon_s=lon_s, lon_e=lon_e)), to_range=to_range)
        # data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    elif data is not None:
        data = data


    data_anomaly = calculate_anomaly(data)
    data_pdo = data.sel(lat=slice(lat_s, lat_e), lon=slice(lon_s, lon_e))
    if remove_trend==remove_trend:
        data_pdo_anomaly = calculate_anomaly(data_pdo, clim_start=clim_start, clim_end=clim_end)
    else:
        data_pdo_anomaly = calculate_anomaly(data_pdo, clim_start=clim_start, clim_end=clim_end) - calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
    # solver=compute_eofs(data_pdo_anomaly, lat_dim='lat')
    solver = compute_rotated_eofs(data_pdo_anomaly, rotated=False, n_modes=1, standardize=None, use_coslat=True)
    return_desired = []
    if remove_trend==False:
        if 'pdo_pattern' in desired:
            return_desired.append(solver.components()[n_modes-1].squeeze())
        if 'pdo_index' in desired:
            return_desired.append(solver.scores()[n_modes-1].squeeze())
        if 'variance_fraction_pdo' in desired:
            return_desired.append(solver.explained_variance_ratio()[n_modes-1].squeeze())
    else:
        if 'pdo_pattern' in desired:
            return_desired.append(solver.components().squeeze())
        if 'pdo_index' in desired:
            return_desired.append(solver.scores().squeeze())
        if 'variance_fraction_pdo' in desired:
            return_desired.append(solver.explained_variance_ratio().squeeze())

    if len(return_desired)==1:
        return return_desired[0]
    else:
        return return_desired




def compute_amo(path=None, var=None, data=None, clim_start=None, clim_end=None, desired=None, start_time=None, end_time=None, lat_s=None, lat_e=None, lon_s=None, lon_e=None, to_range=None):

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
        path (directory): path to data
        var (str): variable name
        start_time (int): start year for the data to be visulaized
        end_time (int): end year for the data to be visulaized
        clim_start: climatology start year
        clim_end: climatology end year (if both None, whole period will be chosen to compute climatology)
        desired: desired variables, can be choosen from 
        ['amo_pattern', 'amo_index'] 
        lat_s = start latitude
        lat_e = end latitude
        lon_s = start longitude
        lon_e = end longitude'''

    if desired==None:
        desired = ['amo_pattern', 'amo_index']

    if to_range==None:
        to_range='0_360'    ## otherwise provide -180_180

    if path is not None and var is not None:

        data = adjust_longitude(rename_dims_to_standard(load_data(path, var, start_time=start_time, end_time=end_time, lat_s=lat_s, lat_e=lat_e, lon_s=lon_s, lon_e=lon_e)), to_range=to_range)
        # data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    elif data is not None:
        data = data

    north_atlantic_sst = data.sel(lat=slice(lat_s, lat_e), lon=slice(lon_s, lon_e))
    

    data_anomalies = calculate_anomaly(north_atlantic_sst, clim_start=clim_start, clim_end=clim_end)
    

    global_mean_data = calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
    

    amo_index = data_anomalies.weighted(compute_weights(data_anomalies)).mean(('lat', 'lon')) - global_mean_data
    

    # if smoothing_window!=None:
    #     amo_index = amo_index.rolling(time=smoothing_window, center=True).mean().dropna(dim='time')
    

    # amo_index = regional_anomaly
    amo_pattern = xr.cov(calculate_anomaly(data), amo_index, dim='time')/amo_index.var()
    return_desired = []
    if 'amo_pattern' in desired:
        return_desired.append(amo_pattern)
    if 'amo_index' in desired:
        return_desired.append(amo_index)
    
    if len(return_desired)==1:
        return return_desired[0]
    else:
        return return_desired


def compute_nao(path=None, var=None, data=None, clim_start=None, clim_end=None, desired=None, lat_s=None, lat_e=None, rotated=None, use_coslat=None, standardize=None, n_modes=2, to_range=None):

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


    if standardize==None:
        standardize=False

    if desired is None:

        desired = ['nao_pattern', 'nao_index', 'variance_fraction_nao']

    if to_range==None:
        to_range='0_360'    ## otherwise provide -180_180

    if path is not None and var is not None:

        data = adjust_longitude(rename_dims_to_standard(load_data(path, var, start_time=start_time, end_time=end_time, lat_s=lat_s, lat_e=lat_e, lon_s=lon_s, lon_e=lon_e)), to_range=to_range)
        # data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    elif data is not None:
        data = data

    north_geop = data.sel(lat=slice(lat_s, lat_e))
    

    data_anomalies = calculate_anomaly(north_geop, clim_start=clim_start, clim_end=clim_end)
    

    nao_index = compute_rotated_eofs(data_anomalies, rotated=rotated, n_modes=n_modes, standardize=standardize, use_coslat=use_coslat).scores()[n_modes-1]

    nao_index = nao_index/nao_index.std()
    
    nao_pattern = compute_rotated_eofs(data_anomalies, rotated=rotated, n_modes=n_modes, standardize=standardize, use_coslat=use_coslat).components()[n_modes-1]

    variance_fraction_nao = compute_rotated_eofs(data_anomalies, rotated=rotated, n_modes=n_modes, standardize=standardize, use_coslat=use_coslat).explained_variance_ratio()[1]
    return_desired = []
    if 'nao_pattern' in desired:
        return_desired.append(nao_pattern.squeeze())
    if 'nao_index' in desired:
        return_desired.append(nao_index.squeeze())
    if 'variance_fraction_nao' in desired:
        return_desired.append(variance_fraction_nao.squeeze())
    
    if len(return_desired)==1:
        return return_desired[0]
    else:
        return return_desired


