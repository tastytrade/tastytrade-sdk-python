from os.path import abspath, join
from sys import path

path.insert(0, abspath(join('..', 'src')))

project = 'tastytrade-sdk'
copyright = '2023, Aaron Mamparo'
author = 'Aaron Mamparo'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary'
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'member-order': 'bysource',
}