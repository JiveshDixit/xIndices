Usage Guide
===========

This section provides examples and guidelines on how to use the `xIndices` module for various calculations, including SST trends, ENSO patterns, and more.

Basic Usage
-----------

Importing the module:

.. code-block:: python

   import xarray as xr
   from xIndices.indices import global_sst_trend_and_enso, compute_nao

Loading Data
------------

To get started, load your SST data into an `xarray.DataArray`:

.. code-block:: python

   data = xr.open_dataset('path_to_your_sst_data.nc')
   sst_data = data['sst']

Calculating SST Trend and ENSO
------------------------------

You can compute the global SST trend and ENSO patterns using the `global_sst_trend_and_enso` function:

.. code-block:: python

   trend_result = global_sst_trend_and_enso(
       data=sst_data, 
       clim_start=1981, 
       clim_end=2010, 
       desired=['sst_trend_pattern', 'enso_pattern', 'enso_index']
   )

   sst_trend_pattern = trend_result[0]
   enso_pattern = trend_result[1]
   enso_index = trend_result[2]

   # Visualize the trend pattern
   sst_trend_pattern.plot()


NAO Index Calculation
---------------------

To compute the NAO index:

.. code-block:: python

   nao_result = compute_nao(
       data=sst_data, 
       clim_start=1981, 
       clim_end=2010, 
       desired=['nao_index', 'nao_pattern', 'variance_fraction_nao']
   )

   nao_index = nao_result[0]
   nao_pattern = nao_result[1]
   nao_var_exp = nao_result[2]

   # Visualize the NAO pattern
   nao_pattern.plot()

Advanced Options
----------------

You can customize the `xIndices` functions with various parameters. For example, to use a different range of longitudes or normalize the results:

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
