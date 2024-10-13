Installation Guide
==================

This section provides instructions for installing the `xIndices` module.

Requirements
------------
- Python 3.10 - 3.12
- numpy >= 1.26, <2.0
- xarray
- xeofs
- xesmf (if needed for regridding)
- Other dependencies can be installed automatically via `pip`.

Installing xIndices
-------------------

You can install `xIndices` directly using `conda` and `pip` both. However, we recommend conda_ driven installation for xIndices_. Run the following command in your terminal:

Using conda (recommended):

.. code-block:: bash

   conda create -n x_indices -c conda forge python=3.11             ##(OPTIONAL)
   conda activate x_indices
   conda install -c jiveshdixit -c conda-forge xindices


Using pip:

.. code-block:: bash

   conda create -n x_indices -c conda forge python=3.11 xesmf       ##(MANDATORY)
   conda activate x_indices
   pip install xIndices



This will download and install the latest version of `xIndices` and its dependencies.

Setting Up the Development Environment
--------------------------------------

If you want to work on `xIndices`'s source code or contribute to its development, you may want to clone the repository and install it in "editable" mode:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/JiveshDixit/xIndices.git
      cd xIndices

2. Create and activate a virtual environment (optional but recommended):

   .. code-block:: bash

      python -m venv env
      source env/bin/activate  # On Windows, use `env\Scripts\activate`


Uninstalling xIndices
---------------------

If you wish to remove `xIndices` from your environment, you can do so using:

.. code-block:: bash

   pip uninstall xIndices
