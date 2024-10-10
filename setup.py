# setup.py

from setuptools import setup, find_packages
import pathlib

# Read the README file
this_dir = pathlib.Path(__file__).parent
long_description = (this_dir / "README.md").read_text()



setup(
    name='xIndices',
    version='1.2.1',
    description='A xarray based module for computing SST trends and SST variability modes and other atmospheric variability modes',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
        'numpy>=1.26, <2.0',
        'dask',
        'xesmf',
        'matplotlib',
        'cartopy',
        'xeofs >2.2.3'
    ],
    python_requires='>=3.10, <3.13'
)
