# xindices/setup.py
from setuptools import setup, find_packages
import pathlib
import os


def read_version():
    """Reads the version from xindices/__init__.py"""
    try:
        with open(os.path.join("xIndices", "__init__.py"), "r") as f:
            for line in f:
                if line.startswith("__version__"):

                    version = line.split("=")[1].strip().strip('"').strip("'")
                    return version
    except FileNotFoundError:
        return "0.0.0"


this_dir = pathlib.Path(__file__).parent
long_description = (this_dir / "README.md").read_text()

setup(
    name='xindices',
    version=read_version(),
    description='A xarray based module for computing SST trends, SST variability modes and other atmospheric variability modes',
    # long_description=long_description,
    # include_package_data=True,
    long_description_content_type='text/markdown',
    author='Jivesh Dixit',
    author_email='jiveshdixit@cas.iitd.ac.in',
    packages=find_packages(where='.', exclude=['tests', 'tests.*', 'docs', 'docs.*']),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        "Intended Audience :: Science/Research",
    ],
    install_requires=[  
        'xarray',
        'numpy>=2.0',
        'dask',
        'xesmf>= 0.7',
        'matplotlib',
        'cartopy',
        'xeofs>2.2.3'
    ],
    python_requires='>=3.11',
    url="https://github.com/JiveshDixit/xindices",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/JiveshDixit/xindices/issues",
        "Documentation": "https://xindices.readthedocs.io/",
        "Source Code": "https://github.com/JiveshDixit/xindices",
    },
)