# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__name__), '..'))

import sphinx_rtd_theme

# Load Version Information
version_dict = {}
with open(os.path.join(os.path.dirname(__file__),
                       '../',
                       'spss_converter',
                       '__version__.py')) as version_file:
    exec(version_file.read(), version_dict)                                     # pylint: disable=W0122

__version__ = version_dict.get('__version__')


# -- Project information -----------------------------------------------------

project = 'SPSS Converter'
copyright = '2021, Insight Industry Inc.'
author = 'Insight Industry Inc.'

# The short X.Y version
version = __version__[:3]
# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx_tabs.tabs'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Autodoc configuration settings.
autoclass_content = 'class'
autodoc_member_order = 'groupwise'
add_module_names = False


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    'navigation_depth': 4,
    'display_version': True,
    'prev_next_buttons_location': 'both'
}

html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "insightindustry", # Username
    "github_repo": "spss-converter", # Repo name
    "github_version": "master", # Version
    "conf_py_path": "/docs/", # Path in the checkout to the docs root
}

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.8', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'validator-collection': ('http://validator-collection.readthedocs.io/en/latest/', None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
