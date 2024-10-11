Usage Guide
===========

This section provides examples and guidelines on how to use the `xIndices` module for various calculations, including SST trends, ENSO patterns, and more.

Basic Usage
-----------

Importing the module:

.. code-block:: python

   from xIndices.preprocess_data import load_data, regridding
   from xIndices.indices import global_sst_trend_and_enso, compute_regional_eof_modes
   from xIndices.utils import line_plot, contour_plot

Loading Data
------------

To get started, load your SST data into an `xarray.DataArray`:

.. code-block:: python

   sst = load_data(path='path_to_file/sst.mnmean.nc', var='sst', start_time=1900, end_time=2020)
   sst_pacific = load_data(path='path_to_file/sst.mnmean.nc', var='sst', start_time=1900, end_time=2020, lat_s=70, lat_e=-20, lon_s=110, lon_e=280)

   
Calculating SST Trend and ENSO
------------------------------

You can compute the global SST trend and ENSO patterns using the `global_sst_trend_and_enso` function:

.. code-block:: python

   trend_result = global_sst_trend_and_enso(
       data=sst, 
       clim_start=1981, 
       clim_end=2010, 
       desired=['sst_trend_pattern', 'enso_pattern', 'enso_index']
   )

   sst_trend_pattern = trend_result[0]
   enso_pattern = trend_result[1]
   enso_index = trend_result[2]

   # Visualize the trend pattern
   contour_plot(sst_trend_pattern, cmap='seismic', levels=list(np.arange(-0.02, 0.021, 0.001)), extend='both', central_lon=180)
   line_plot(enso_index, color='r', label='ENSO index')


Customized region variability Calculation
-----------------------------------------

To compute variability mode in customized region:

.. code-block:: python

   sst_pacific_modes = compute_regional_eof_modes(
       data=sst_pacific, 
       clim_start=1981, 
       clim_end=2010,
       rotated=None,
       n_modes=2,
       remove_trend=True,
       desired=['regional_patterns', 'regional_timeseries']
   )

   pacific_modes_index = sst_pacific_modes[0]
   pacific_modes_pattern = sst_pacific_modes[1]

   # Visualize the pacific 1st mode pattern
   contour_plot(pacific_modes_pattern[0], cmap='seismic', levels=list(np.arange(-0.02, 0.021, 0.001)), extend='both', central_lon=180)


   # Visualize the pacific 2nd mode index
   line_plot(pacific_modes_index[1], color='r', label='Pacific 2nd mode index')


NAO Calculation
---------------

To compute NAO patterns and index:

.. code-block:: python

   z = load_data(path='path_to_file/geopotential.height.nc', var='z', start_time=1900, \
   end_time=2020, lat_s=90, lat_e=20)
   sst_pacific_modes = compute_nao(
       data=sst, 
       clim_start=1981, 
       clim_end=2010,
       rotated='Varimax',
       nao_mode=1       ## Assuming NAO mode is the first mode otherwise change this
       desired=['nao_index', 'nao_pattern', 'variance_fraction_nao']
   )

   nao_index = nao_result[0]
   nao_pattern = nao_result[1]
   nao_var_exp = nao_result[2]

   # Visualize the NAO pattern and index
   contour_plot(nao_pattern, cmap='seismic', levels=list(np.arange(-0.02, 0.021, 0.001)), \
   extend='both', central_lon=180)
   line_plot(nao_index=, color='r', label='NAO index', variance_fraction=nao_var_exp)   
   ### defining variance_fraction will print variance fraction upto 2 decimal places

Advanced Options
----------------

You can customize the `xIndices` functions with various parameters. For example, to use a different range of longitudes or normalize the results, refer to docs for options for each functions:

.. code-block:: python

   result = indices.global_sst_trend_and_enso(
       data=sst_data,
       clim_start=1981,
       clim_end=2010,
       to_range='-180_180',
       standardize=True,
       normalize_pattern=True,
       normalize_index=False
   )
