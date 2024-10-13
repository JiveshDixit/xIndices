xIndices
========

This section provides an overview of the modules included in the `xIndices` package and their functionalities.

.. toctree::
   :maxdepth: 4
   :caption: API Documentation


Overview
--------

`xIndices` is organized into the following modules:

1. **xIndices.indices**: 
   This module contains functions for calculating indices such as SST trends, ENSO patterns, MJO phase diagrams, and NAO indices.

   - `global_sst_trend_and_enso`: Calculate global SST trend, warming patterns, ENSO patterns, and indices.
   - `compute_nao`: Compute the NAO index and pattern using EOF analysis using varimax rotation.
   - `compute_pdo`: Calculate PDO indices and pattern usin EOF analysis.
   - `compute_amo`: Calculate PDO indices and pattern using area-averaged detrended anomaly
   - `compute_regional_eof_modes`: Calculate regional EOF modes (Rotated and unrotated) from gridded data.

2. **xIndices.preprocess_data**: 
   This module handles data preprocessing tasks, such as calculating climatological anomalies and preparing data for EOF analysis.

   - `load_data`: Load NetCDF data into `xarray` DataArrays.
   - `write_netcdf`: Save processed data back to NetCDF format.
   - `regridding`: It helps regrid the Datasets and dataArrays (Curvilinear to Rectilinear; Rectilinear to Rectilinear) 
   - `adjust_longitude`: Helper function and user function to adjust the longitude range of the dataset.
   - `rename_dims_to_standard`: Helper function and user function to rename dimensions to standard names for easier processing.

3. **xIndices.utils**: 
   Contains utility functions that assist with common tasks required in data processing and analysis.

   - `calculate_anomaly`: Helper function to calculate anomalies based on a specified climatological period.
   - `compute_weights`: Helper function to compute latitudinal area weights.
   - `compute_rotated_eofs`: Compute EOFs with optional rotation using Varimax or Promax methods.
   - `line_plot`: Help visulize 1D data such as indices or PCs
   - `contour_plot`: Help visulize 2D data such as patterns or EOFs


Detailed Documentation
----------------------

xIndices package
================

Submodules
----------

xIndices.indices module
-----------------------

.. automodule:: xIndices.indices
   :members:
   :undoc-members:
   :show-inheritance:


xIndices.preprocess\_data module
--------------------------------

.. automodule:: xIndices.preprocess_data
   :members:
   :undoc-members:
   :show-inheritance:

xIndices.utils module
---------------------

.. automodule:: xIndices.utils
   :members:
   :undoc-members:
   :show-inheritance:

Module contents
---------------

.. automodule:: xIndices
   :members:
   :undoc-members:
   :show-inheritance:


