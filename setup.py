# setup.py

from setuptools import setup, find_packages

setup(
    name='xIndices',
    version='0.1.0',
    description='A xarray based module for computing SST trends and SST variability modes and other atmospheric variability modes',
    author='Jivesh Dixit',
    author_email='jiveshdixit@cas.iitd.ac.in',
    packages=find_packages(),
    classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    'Topic :: Communications :: Email'],
    install_requires=[
        'xarray',
        'numpy',
        'xesmf',
        'eofs',
        'dask',
        'xesmf',
        'matplotlib',
        'cartopy',
        'xeofs'
    ],
    python_requires='>=3.8',
)
