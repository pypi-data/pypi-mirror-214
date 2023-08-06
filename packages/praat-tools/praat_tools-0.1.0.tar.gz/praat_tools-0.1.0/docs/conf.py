import os

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'praat-tools'
copyright = '2023, Athena Luka'
author = 'Athena Luka'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.intersphinx', 'sphinx.ext.autodoc']

autodoc_member_order = 'bysource'
autoclass_content = "both"
autodoc_typehints = 'description'
autodoc_inherit_docstrings = False

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
