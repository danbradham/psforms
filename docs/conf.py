# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import psforms

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
]

source_suffix = '.rst'
master_doc = 'index'
project = psforms.__title__
copyright = u'2015, {0}'.format(psforms.__author__)
version = psforms.__version__
release = psforms.__version__
pygments_style = 'sphinx'
intersphinx_mapping = {'http://docs.python.org/': None}
