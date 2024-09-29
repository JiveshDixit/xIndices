# xIndices
xIndices: SST trends and variability using xarray

https://pypi.org/project/xIndices/

This package is based on xarray to analyse various climate variability modes; patterns and indices. This can be installed using pip to an existing xarray, xesmf environment or a new envioronment with xesmf installed using conda (to include esmpy in the installation).

Install this package using,

pip install xIndices

SST warming trend and ENSO are calculated in this package as first and second mode of global sst variability. PDO, AMO and NAO modes can also be calculated using this. We are commited to add more important climate variability modes as the competency of this package. It can preprocess the data including regridding, rearranging the dimesnions, renaming the dimensions of the xarray.DataArray or xarray.Dataset. We can also visualize the timeseries in this package. We shall be including the capability to visualize the patterns of the variability within the package itself.
