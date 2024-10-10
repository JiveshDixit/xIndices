# eof_calculations.py

import numpy as np
from .utils import calculate_anomaly, compute_weights, compute_rotated_eofs
import xarray as xr
from .preprocess_data import load_data, rename_dims_to_standard, adjust_longitude



def calculate_global_mean_sst(data, lat_name='lat', lon_name='lon'):
    return calculate_anomaly(data).weighted(compute_weights(data)).mean(dim=[lat_name, lon_name])



def global_sst_trend_and_enso(data=None, path=None, var=None, clim_start=None, clim_end=None, desired=None, 
    start_time=None, end_time=None, to_range='0_360', standardize=False, 
    normalize_pattern=True, normalize_index=False):
    """
    Calculate global SST warming trend and ENSO patterns using EOF analysis.

    This function computes the global SST warming trend, ENSO index, and their
    corresponding variance fractions using the first two EOF modes of SST anomalies.
    It first removes the annual cycle climatology and then applies EOF analysis.

    Parameters:
    ----------
    data : xarray.DataArray or xarray.Dataset, optional
        Gridded SST data with dimensions (time, lat, lon). If not provided, 
        'path' and 'var' must be used to load the data.
    path : str, optional
        Directory path to the data. Required if 'data' is not provided.
    var : str, optional
        Name of the variable to load from the dataset.
    clim_start : int, optional
        Climatology start year.
    clim_end : int, optional
        Climatology end year (if both None, the entire period is used for climatology).
    desired : list of str, optional
        Desired outputs, which can include:
        ['sst_trend_pattern', 'sst_trend_timeseries', 'variance_fraction_trend', 
        'enso_pattern', 'enso_index', 'variance_fraction_enso']. 
        Default is to return all.
    start_time : int, optional
        Start year for loading data.
    end_time : int, optional
        End year for loading data.
    to_range : str, optional, default '0_360'
        Longitude range for data adjustment. Options are '0_360' or '-180_180'.
    standardize : bool, optional, default False
        Whether to normalize the data with its standard deviation before EOF calculation.
    normalize_pattern : bool, optional, default True
        Whether to normalize spatial components (patterns) with singular values.
    normalize_index : bool, optional, default False
        Whether to normalize time series (scores) with singular values.

    Returns:
    -------
    List containing the desired outputs: SST trend pattern, trend timeseries,
    variance fraction of the trend, ENSO pattern, ENSO index, and variance fraction of ENSO.
    """


    if desired is None:
        desired = [
            'sst_trend_pattern', 'sst_trend_timeseries', 'variance_fraction_trend',
            'enso_pattern', 'enso_index', 'variance_fraction_enso'
        ]
    

    if path and var:
        data = adjust_longitude(
            rename_dims_to_standard(
                load_data(path, var, start_time=start_time, end_time=end_time)
            ),
            to_range=to_range
        )
    

    data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)


    solver = compute_rotated_eofs(
        data_anom, rotated=False, n_modes=2, standardize=standardize, use_coslat=True
    )
    

    eofs_ = solver.components(normalized=normalize_pattern)
    pcs_ = solver.scores(normalized=normalize_index)
    var_frac_ = solver.explained_variance_ratio()


    result_dict = {
        'sst_trend_pattern': eofs_[0].squeeze(),
        'sst_trend_timeseries': (pcs_[0] / pcs_[0].std()).squeeze(),
        'variance_fraction_trend': var_frac_[0].squeeze(),
        'enso_pattern': eofs_[1].squeeze(),
        'enso_index': (pcs_[1] / pcs_[1].std()).squeeze(),
        'variance_fraction_enso': var_frac_[1].squeeze()
    }

    return_desired = [result_dict[key] for key in desired if key in result_dict]
    return return_desired[0] if len(return_desired) == 1 else return_desired



def compute_regional_eof_modes(data=None, path=None, var=None, clim_start=None, clim_end=None, desired=None, 
    start_time=None, end_time=None, lat_s=90, lat_e=-90, lon_s=0, lon_e=360, 
    to_range='0_360', n_modes=1, remove_trend=False, rotated=False, 
    use_coslat=True, standardize=False, normalize_pattern=True, normalize_index=False):
    """
    Calculate regional EOF (Empirical Orthogonal Functions) modes from gridded SST data.

    This generalized function computes EOFs for a specified regional domain, allowing for 
    trend removal, rotation, and different normalization options.

    Parameters:
    ----------
    data : xarray.DataArray or xarray.Dataset, optional
        Gridded SST data with dimensions (time, lat, lon). Use 'path' and 'var' 
        instead if you want to load the data from a file.
    path : str, optional
        Directory path to the data. Required if 'data' is not provided.
    var : str, optional
        Name of the variable to load from the dataset.
    clim_start : int, optional
        Climatology start year.
    clim_end : int, optional
        Climatology end year (if both None, the entire period is used for climatology).
    desired : list, optional
        Desired outputs, which can be ['regional_patterns', 'regional_timeseries', 
        'variance_fractions_regional']. Default is all three.
    start_time : int, optional
        Start year for loading data.
    end_time : int, optional
        End year for loading data.
    lat_s : float, optional
        Start latitude for the regional selection. Default is 90.
    lat_e : float, optional
        End latitude for the regional selection. Default is -90.
    lon_s : float, optional
        Start longitude for the regional selection. Default is 0.
    lon_e : float, optional
        End longitude for the regional selection. Default is 360.
    to_range : str, optional
        Target longitude range. Default is '0_360'. Use '-180_180' if needed.
    n_modes : int, optional
        Number of EOF modes to compute. Default is 1.
    remove_trend : bool, optional
        Whether to remove the global trend before calculating EOFs. Default is False.
    rotated : bool, optional
        Whether to apply Varimax or Promax rotation to the EOFs. Default is False.
    use_coslat : bool, optional
        Whether to use cosine latitude weighting. Default is True.
    standardize : bool, optional
        Whether to normalize the data with its standard deviation before EOF calculation. Default is False.
    normalize_pattern : bool, optional
        Whether to normalize spatial components (patterns) with singular values. Default is True.
    normalize_index : bool, optional
        Whether to normalize the time series (scores) with singular values. Default is False.

    Returns:
    -------
    List containing the desired outputs: regional patterns, timeseries, and/or variance fractions.
    """

    if desired is None:
        desired = ['regional_patterns', 'regional_timeseries', 'variance_fractions_regional']
    

    if path and var:
        data = adjust_longitude(
            rename_dims_to_standard(
                load_data(
                    path, var, start_time=start_time, end_time=end_time, 
                    lat_s=lat_s, lat_e=lat_e, lon_s=lon_s, lon_e=lon_e
                )
            ),
            to_range=to_range
        )
    

    data_anom = calculate_anomaly(data, clim_start=clim_start, clim_end=clim_end)
    if remove_trend:
        global_mean_sst = calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
        data_anom -= global_mean_sst


    solver = compute_rotated_eofs(
        data_anom, rotated=rotated, n_modes=n_modes, 
        standardize=standardize, use_coslat=use_coslat
    )


    result_dict = {
        'regional_patterns': solver.components(normalized=normalize_pattern).squeeze(),
        'regional_timeseries': (solver.scores(normalized=normalize_index) / 
                                solver.scores(normalized=normalize_index).std()).squeeze(),
        'variance_fractions_regional': solver.explained_variance_ratio().squeeze()
    }


    return_desired = [result_dict[key] for key in desired if key in result_dict]
    return return_desired[0] if len(return_desired) == 1 else return_desired




def compute_pdo(data=None, path=None, var=None, clim_start=None, clim_end=None, desired=None, 
    start_time=None, end_time=None, to_range='0_360', standardize=False, 
    normalize_pattern=True, normalize_index=False, lat_s=70, lat_e=20, lon_s=110, 
    lon_e=260, remove_trend=False):
    """
    Calculate the PDO (Pacific Decadal Oscillation) index and pattern.

    This function calculates the conventional PDO index, pattern, and variance fraction 
    as the first EOF modes of SST anomaly in the North Pacific (above 20°N) after 
    removing the annual cycle climatology and global mean SST (to account for the warming trend).

    Parameters:
    ----------
    data : xarray.DataArray or xarray.Dataset, optional
        Gridded SST data with dimensions (time, lat, lon). Use 'path' and 'var' 
        instead if you want to load the data from a file.
    path : str, optional
        Directory path to the data. Required if 'data' is not provided.
    var : str, optional
        Name of the variable to load from the dataset.
    clim_start : int, optional
        Climatology start year.
    clim_end : int, optional
        Climatology end year (if both None, whole period will be chosen for climatology).
    desired : list, optional
        Desired outputs, which can be ['pdo_pattern', 'pdo_index', 'variance_fraction_pdo']. 
        Default is all three.
    start_time : int, optional
        Start year for loading data.
    end_time : int, optional
        End year for loading data.
    to_range : str, optional
        Target longitude range. Default is '0_360'. Use '-180_180' if needed.
    standardize : bool, optional
        Whether to normalize the data with its standard deviation.
    normalize_pattern : bool, optional
        Whether to normalize spatial components with singular values. Default is True.
    normalize_index : bool, optional
        Whether to normalize the time series (scores) with singular values. Default is False.
    remove_trend : bool, optional
        Whether to remove the global trend. Default is False, in which case mode 2 is used. 
        If True, mode 1 is used.

    Returns:
    -------
    List containing the desired outputs: PDO pattern, PDO index, and/or variance fraction.
    """

    if desired is None:
        desired = ['pdo_pattern', 'pdo_index', 'variance_fraction_pdo']
    

    n_modes = 1 if remove_trend else 2
    

    if path and var:
        data = adjust_longitude(
            rename_dims_to_standard(
                load_data(
                    path, var, start_time=start_time, end_time=end_time, 
                    lat_s=lat_s, lat_e=lat_e, lon_s=lon_s, lon_e=lon_e
                )
            ),
            to_range=to_range
        )


    data_anomaly = calculate_anomaly(data)
    data_pdo = data_anomaly.sel(lat=slice(lat_s, lat_e), lon=slice(lon_s, lon_e))
    

    if remove_trend:
        data_pdo_anomaly = data_pdo - calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
    else:
        data_pdo_anomaly = calculate_anomaly(data_pdo, clim_start=clim_start, clim_end=clim_end)
    

    solver = compute_rotated_eofs(
        data_pdo_anomaly, rotated=False, n_modes=n_modes, 
        standardize=standardize, use_coslat=True
    )
    

    result_dict = {
        'pdo_pattern': solver.components()[n_modes - 1].squeeze(),
        'pdo_index': (solver.scores()[n_modes - 1] / solver.scores()[n_modes - 1].std()).squeeze(),
        'variance_fraction_pdo': solver.explained_variance_ratio()[n_modes - 1].squeeze()
    }
    

    return_desired = [result_dict[key] for key in desired if key in result_dict]
    return return_desired[0] if len(return_desired) == 1 else return_desired



def compute_amo(data=None, path=None, var=None, clim_start=None, clim_end=None, desired=None, 
    start_time=None, end_time=None, lat_s=70, lat_e=0, lon_s=280, lon_e=360, 
    to_range='0_360'):
    """
    Calculate the AMO (Atlantic Multidecadal Oscillation) index and pattern.

    This function calculates the conventional AMO index and AMO pattern as the 
    area-averaged SST anomalies and time-averaged SST anomalies in the North Atlantic 
    (0°N-70°N) after removing the annual cycle climatology and global mean SST (to 
    account for the warming trend).

    Parameters:
    ----------
    data : xarray.DataArray or xarray.Dataset, optional
        Gridded SST data with dimensions (time, lat, lon). Use 'path' and 'var' 
        instead if you want to load the data from a file.
    path : str, optional
        Directory path to the data. Required if 'data' is not provided.
    var : str, optional
        Name of the variable to load from the dataset.
    start_time : int, optional
        Start year for loading data.
    end_time : int, optional
        End year for loading data.
    clim_start : int, optional
        Climatology start year.
    clim_end : int, optional
        Climatology end year (if both None, whole period will be chosen for climatology).
    desired : list, optional
        Desired outputs, which can be ['amo_pattern', 'amo_index']. Default is both.
    lat_s : float, optional
        Start latitude for the region. Default is 70 (North).
    lat_e : float, optional
        End latitude for the region. Default is 0 (Equator).
    lon_s : float, optional
        Start longitude for the region. Default is 280 (Western Atlantic).
    lon_e : float, optional
        End longitude for the region. Default is 360.
    to_range : str, optional
        Target longitude range. Default is '0_360'. Use '-180_180' if needed.

    Returns:
    -------
    List containing the desired outputs: AMO pattern and/or AMO index.
    """

    if desired is None:
        desired = ['amo_pattern', 'amo_index']


    if path is not None and var is not None:
        data = adjust_longitude(
            rename_dims_to_standard(
                load_data(path, var, start_time=start_time, end_time=end_time)
            ),
            to_range=to_range
        )


    north_atlantic_sst = data.sel(lat=slice(lat_s, lat_e), lon=slice(lon_s, lon_e))
    

    data_anomalies = calculate_anomaly(
        north_atlantic_sst, clim_start=clim_start, clim_end=clim_end
    )
    

    global_mean_data = calculate_global_mean_sst(data, lat_name='lat', lon_name='lon')
    

    amo_index = (
        data_anomalies.weighted(compute_weights(data_anomalies)).mean(('lat', 'lon')) 
        - global_mean_data
    )
    

    amo_pattern = (
        xr.cov(calculate_anomaly(data), amo_index, dim='time') 
        / amo_index.var()
    )
    

    result_dict = {
        'amo_pattern': amo_pattern,
        'amo_index': amo_index
    }
    

    return_desired = [result_dict[key] for key in desired if key in result_dict]
    return return_desired[0] if len(return_desired) == 1 else return_desired



def compute_nao(data=None, path=None, var=None, clim_start=None, clim_end=None, desired=None, 
    lat_s=None, lat_e=None, use_coslat=None, standardize=None, to_range=None, n_modes=10, nao_mode=None,
    start_time=None, end_time=None, rotated='Varimax'):
    '''
    This function calculates the NAO index, NAO pattern, and variance fraction.
    It is calculated as the second EOF mode of 500mb geopotential height 
    anomaly above 20N after removing the annual cycle climatology.

    Parameters:
    - data : xarray.DataArray or xarray.Dataset
        Processed gridded data in the shape of (time, lat, lon).
    
    - path : str, optional
        Path to the data file (if data is to be loaded directly).
    
    - var : str, optional
        Variable name in the dataset (used if loading from a file).
    
    - clim_start : int, optional
        Climatology start year.
    
    - clim_end : int, optional
        Climatology end year. If None, the whole period will be used.
    
    - desired : list, optional
        List of desired outputs, e.g., ['nao_pattern', 'nao_index', 'variance_fraction_nao'].
    
    - lat_s : float, optional
        Start latitude for selecting the northern region.
    
    - lat_e : float, optional
        End latitude for selecting the northern region.
    
    - use_coslat : bool, optional
        Whether to apply cosine latitude weighting. Default is True.
    
    - standardize : bool, optional
        If True, standardizes the data. Default is False.
    
    - to_range : str, optional
        Longitude range, either '0_360' or '-180_180'. Default is '0_360'.
    
    - nao_mode : int, optional
        The EOF mode number to be considered as NAO. Default is 1.
    
    - start_time, end_time : str, optional
        Time range for selecting data.
    
    - rotated : str, optional
        Rotation method for EOFs. Options: None, 'Varimax', 'Promax'. Default is 'Varimax'.
    '''
    

    lat_s = lat_s if lat_s is not None else 90
    lat_e = lat_e if lat_e is not None else 20
    standardize = standardize if standardize is not None else False
    desired = desired if desired is not None else ['nao_pattern', 'nao_index', 'variance_fraction_nao']
    to_range = to_range if to_range is not None else '0_360'
    nao_mode = nao_mode if nao_mode is not None else 1


    if path is not None and var is not None:
        data = adjust_longitude(rename_dims_to_standard(
            load_data(path, var, start_time=start_time, end_time=end_time, lat_s=lat_s, lat_e=lat_e)
        ), to_range=to_range)


    if data is None:
        raise ValueError("Data must be provided either directly or via path and var.")

    north_geop = data.sel(lat=slice(lat_s, lat_e))
    

    data_anomalies = calculate_anomaly(north_geop, clim_start=clim_start, clim_end=clim_end)
    

    eofs_result = compute_rotated_eofs(
        data_anomalies, rotated=rotated, n_modes=n_modes, 
        standardize=standardize, use_coslat=use_coslat
    )


    nao_index = eofs_result.scores()[nao_mode-1] / eofs_result.scores()[nao_mode-1].std()
    nao_pattern = eofs_result.components()[nao_mode-1]
    variance_fraction_nao = eofs_result.explained_variance_ratio()[nao_mode-1]
    
    result_dict = {
        'nao_pattern': nao_pattern.squeeze(),
        'nao_index': nao_index.squeeze(),
        'variance_fraction_nao': variance_fraction_nao.squeeze(),
    }
    

    return_desired = [result_dict[key] for key in desired if key in result_dict]
    return return_desired[0] if len(return_desired) == 1 else return_desired

