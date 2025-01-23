# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

project = 'hello-whorl'
copyright = '2025 hello-whorl'
author = 'Preston Smith, Aidan Dyga, Rebekah Rudd, Jason Gyamafi'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

language = 'python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_theme_options = {
    "light_css_variables": {
        # Background colors
        "color-background-primary": "#262932",  # Main content background
        "color-background-secondary": "#262932", # Sidebar background
        
        # Text colors
        "color-foreground-primary": "#ffffff", # Main text color
        "color-foreground-secondary": "#e0b027", # Secondary text color
        
        # Link colors
        "color-brand-primary": "#e69824", # Primary brand color
        "color-brand-content": "#e69824", # Link color
        
        # Sidebar colors
        "color-sidebar-link-text": "#e0b027", # Sidebar link color
        "color-sidebar-link-text--top-level": "#e69824", # Top level sidebar links
        
        # API/Code colors
        "color-api-name": "#e69824", # Function names
        "color-api-pre-name": "#e69824", # Class/module names
    },
}