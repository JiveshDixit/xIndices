import xarray as xr
from SST_indices import compute_sst_trend_enso, compute_pdo

# Load SST data
sst = xr.open_dataset('./..Indices/sst.mnmean.nc')['sst']

# Define climatology period
clim_start = 1981
clim_end = 2010

# Compute SST trend and ENSO
sst_trend_pattern, enso_pattern, sst_trend_ts, enso_index = compute_sst_trend_enso(sst, clim_start, clim_end)

# Compute PDO
pdo_pattern, pdo_index = compute_pdo(sst, clim_start, clim_end)