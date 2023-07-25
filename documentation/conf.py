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
import os
import sys
sys.path.insert(0, os.path.abspath(".."))

# import sphinx_rtd_theme

# -- Project information -----------------------------------------------------

project = "PySILLS"
copyright = "2023, Maximilian A. Beeskow"
author = "Maximilian A. Beeskow"

# The full version, including alpha/beta/rc tags
release = "v.1.1.0-beta"
version = release

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    #'nbsphinx',
    #'sphinx_book_theme',
    #'sphinx.ext.autodoc',
    #'sphinx.ext.napoleon',
    #'sphinx.ext.doctest',
    #'sphinx.ext.autosummary',
    #'sphinx_markdown_tables',
    # 'notfound.extension',
    #'sphinx_copybutton',
    #'sphinx_gallery.gen_gallery',
    #'sphinx.ext.extlinks',
    #'sphinx.ext.coverage',
    #'sphinx.ext.mathjax',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = "sphinx_book_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

html_title = "PySILLS - LA-ICP-MS data reduction for minerals and fluid/melt inclusions"
html_logo = "documentation/images/PySILLS_Logo_GitHub.png"
#html_favicon = ""

#nbsphinx_execute = "never"

#nbsphinx_execute_arguments = [
#    "--InlineBackend.figure_formats={'svg', 'pdf'}",
#    "--InlineBackend.rc={'figure.dpi': 96}",
]

copybutton_prompt_text = ">>> "