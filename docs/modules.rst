Modules
=======

This section provides an overview of the modules included in the `xIndices` package and their functionalities.

.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   xIndices/indices
   xIndices/preprocess_data
   xIndices/utils
   xIndices/main

Overview
--------

`xIndices` is organized into the following modules:

1. **xIndices.indices**: 
   This module contains functions for calculating indices such as SST trends, ENSO patterns, MJO phase diagrams, and NAO indices.

   - `global_sst_trend_and_enso`: Calculate global SST trend, warming patterns, ENSO patterns, and indices.
   - `compute_nao`: Compute the NAO index and pattern using EOF analysis using varimax rotation.
   - `compute_pdo`: Calculate PDO indices and pattern usin EOF analysis.
   - `compute_amo`: Calculate AMO indices and pattern using area-averaged detrended anomaly
   - `compute_regional_eof_modes`: Calculate regional EOF modes (Rotated and unrotated) from gridded data.

2. **xIndices.preprocess_data**: 
   This module handles data preprocessing tasks, such as calculating climatological anomalies and preparing data for EOF analysis.


   - `load_data`: Load NetCDF data into `xarray` DataArrays.
   - `write_netcdf`: Save processed data back to NetCDF format.
   - `regridding`: Regridding data from curvilinear or rectilinear grid to rectilinear grid.
   - `adjust_longitude`: Adjust the longitude range of the dataset.
   - `rename_dims_to_standard`: Rename dimensions to standard names for easier processing.

3. **xIndices.utils**: 
   Contains utility functions that assist with common tasks required in data processing and analysis.

   - `calculate_anomaly`: Calculate anomalies based on a specified climatological period.
   - `compute_rotated_eofs`: Compute EOFs with optional rotation using Varimax or Promax methods.
   - `line_plot`: Help visulize 1D data such as indices or PCs
   - `contour_plot`: Help visulize 2D data such as patterns or EOFs


Detailed Documentation
----------------------

.. toctree::
   :maxdepth: 2
   :caption: API Documentation

Below are detailed descriptions of the modules and their functions. Click on each to view the complete documentation:

.. automodule:: xIndices.indices
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: xIndices.preprocess_data
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: xIndices.utils
   :members:
   :undoc-members:
   :show-inheritance:
