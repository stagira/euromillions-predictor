# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# docs/conf.py
import os
import sys
# On remonte d'un niveau pour que Sphinx voie le dossier racine du projet
sys.path.insert(0, os.path.abspath('..'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Euromillions Predictor'
copyright = '2025, Philippe Hermoso'
author = 'Philippe Hermoso'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Le coeur de l'autodocumentation
    'sphinx.ext.napoleon',     # Pour comprendre les docstrings style Google
    'sphinx.ext.viewcode',     # Ajoute un lien vers le code source
    'sphinx_autodoc_typehints',# Pour bien afficher les type hints
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
