import os
import sys


sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../et_engine_cli'))

project = 'ET Engine Command Line Interface'
copyright = '2024, Exploration Technologies, Inc.'
author = 'Exploration Technologies, Inc.'
release = '0.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx_click',
    'sphinx.ext.intersphinx'
]

html_theme = 'furo'
html_show_sourcelink = False
html_copy_source = False
html_show_sphinx = False

autosummary_imported_members = True
autosummary_generate = True
autodoc_member_order = 'groupwise'
autosummary_depth = 2

autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'show-inheritance': False,
    'show-source': False,
    'private-members': False,
    'no-special-members': True
}

html_static_path = ['_static']
html_css_files = ['custom.css']
