.. image:: ./xIndices.png
  :class: only-dark
  :align: center
  :width: 250
  :alt: logo of xIndices


.. image:: ./xIndices.png
  :class: only-light
  :align: center
  :width: 250
  :alt: logo of xIndices



.. rst-class:: center

Welcome to xIndices's documentation!
====================================


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Contents:

   installation
   usage
   api
   modules

xIndices is a Python package developed for computing climte variability modes using dimensionality reduction and area-averaging methods. It can help us make sense of noisy large datasets by extracting meaningful and identified patterns. Combining the capabilities of xarray_, Dask_ and xeofs_, it enables efficient handling and scalable computation of large, multi-dimensional datasets. Smart collaboration of these modules with scientific definitions of variability modes can help people interested in indices and patterns without diving into the mathematics and definitions.

.. grid:: 2

    .. grid-item-card:: 
      :octicon:`gear;10em`
      :link: installation
      :link-type: doc
      :text-align: center

      **Installation**
      Get started with xIndices.
      

    .. grid-item-card::
      :octicon:`repo;10em`
      :link: usage
      :link-type: doc
      :text-align: center

      **User Guide**
      Learn more about the package and its features.
      
.. grid:: 2

    .. grid-item-card::
      :octicon:`search;10em`
      :link: api
      :link-type: doc
      :text-align: center

      **API Reference**

      Explore the available submodules and functions.



.. _xarray: https://docs.xarray.dev/en/stable/index.html
.. _Dask: https://dask.org/
.. _xeofs: https://xeofs.readthedocs.io/en/latest/index.html
