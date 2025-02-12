# __init__.py

__version__ = "1.3.6"

from .utils import calculate_anomaly, compute_weights, line_plot, compute_rotated_eofs, contour_plot, lanczos_filter_xarray,\
		standardize_data, project_data_onto_eofs, stack_vars
from .indices import global_sst_trend_and_enso, compute_pdo, compute_amo, compute_regional_eof_modes, compute_nao
from .preprocess_data import load_data, write_netcdf, regridding, adjust_longitude, \
		rename_dims_to_standard, adjust_latitude