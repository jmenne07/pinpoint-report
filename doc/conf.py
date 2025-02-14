# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import django

sys.path.insert(0, os.path.abspath(".."))
os.environ["DJANGO_SETTINGS_MODULE"] = "pinpoint_report.settings"
django.setup()

project = "Pinpoint-Report"
copyright = "2025, Jörn Menne"
author = "Jörn Menne"
release = "0.1.6"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.duration",
    "sphinx.ext.napoleon",
    "sphinxcontrib.plantuml",
    "sphinxcontrib.mermaid",
    "sphinx.ext.mathjax",
    "myst_parser",
    "sphinx.ext.todo",
    "sphinx.ext.autosectionlabel",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]


# Options for todo
todo_include_todos = True
