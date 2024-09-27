# setup.py

from setuptools import setup, find_packages

setup(
    name='xIndices',
    version='0.2',
    description='A module for computing SST trends and variability',
    author='Jivesh Dixit',
    author_email='jiveshdixit@cas.iitd.ac.in',
    packages=find_packages(),
    install_requires=[
        'xarray',
        'numpy',
        'xesmf',
        'eofs',
        'dask'
    ],
    python_requires='>=3.6',
)
