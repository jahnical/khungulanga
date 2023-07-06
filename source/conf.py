# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import django

project = 'Khungulanga'
copyright = '2023, ICT GROUP 7'
author = 'ICT GROUP 7'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add sphinxcontrib_django to installed extensions
extensions = [
    'sphinx.ext.autodoc',
    "sphinxcontrib_django",
    "sphinx_bootstrap_theme"
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'bootstrap'
html_static_path = ['staticfiles']

# Add source directory to sys.path
sys.path.insert(0, os.path.abspath("../"))

# Configure the path to the Django settings module
django_settings = "smartskin.settings"
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartskin.settings'
django.setup()