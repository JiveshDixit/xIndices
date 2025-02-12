**xIndices: A xarray based module for computing SST trends, SST variability modes and other atmospheric variability modes**

[![PyPi Shield](https://img.shields.io/pypi/v/xIndices)](https://pypi.org/project/xIndices/)

[![Downloads](https://img.shields.io/pepy/dt/xIndices)](https://img.shields.io/pepy/dt/xIndices)

# Overview

**xIndices** is a xarray based Python library for calculating climate variability indices and patterns.
For now, from preprocessing the data to final calculation of indices and patterns, it allows user to directly
calculate without diving into the steps for calculations.
**Key Features:**

* **Load, pre-process and Regrid** Multiple data preprocessing tools are already supported including 
using ESMF defined methods. 

* **Rotated EOF analysis** This also allows user to examine EOF modes (Rotated: Varimax and Promax & Unrotated) 
in user defined regions. Returns the desired number of modes (PCs and EOFs along with their variance explained 
in the data). This comes in handy when one wants to play around EOF patterns in user selected regions and variables.  

* **Various Climate variability modes and warming trend** Right now, we support SST Warming mode, ENSO mode using 
global SST (One can calculate other modes using generaic EOF tool of this package), PDO, AMO, NAO etc. We intend to
add more variability modes.


# Install





Install the xIndices library using pip or conda.

```bash
conda create -n x_indices python=3.11 (OPTIONAL)
conda activate x_indices (If creating the x_indices environment)
conda install -c jiveshdixit -c conda-forge xindices
```

```bash
conda create -n x_indices python=3.11 xesmf (MANDATORY)
conda activate x_indices
pip install xIndices
```

# Update

I have added Lanczos filter, correction for error due to 
latitude ascending, added some more support functions such 
as standardize variable, stack variables, Projectdata onto eofs etc.
Some small bugs has also been addressed, however, they didn't affect 
the accuracy of analysis eralier


# Community & Support

For now we have a Slack community page for comments, suggestions and error reporting. 

[![Community](https://xindices.slack.com)](https://xindices.slack.com)

