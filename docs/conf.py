# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'xIndices'
copyright = '2024, Jivesh Dixit'
author = 'Jivesh Dixit'
release = '1.2.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.mathjax',
              'sphinx.ext.viewcode',
              'sphinx.ext.autosummary',
              'sphinx.ext.intersphinx',
              'sphinx.ext.extlinks',
              'matplotlib.sphinxext.plot_directive',
              'sphinx_issues',]

html_sidebars = {'**': ['sidebar_toc.html',
                        'relations.html',
                        'sourcelink.html',
                        'searchbox.html']}

autosummary_generate = True  # Turn on sphinx.ext.autosummary
templates_path = ['_templates']
exclude_patterns = []

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

html_logo = "./logo.jpeg"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
