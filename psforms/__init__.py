# -*- coding: utf-8 -*-

__title__ = 'psforms'
__author__ = 'Dan Bradham'
__email__ = 'danielbradham@gmail.com'
__url__ = 'http://github.com/danbradham/apptemplate.git'
__version__ = '0.1.1'
__license__ = 'MIT'
__description__ = '''psforms'''

import os

from . import resource
from . import controls
from .exc import (FormNotInstantiated, FieldNotFound, FieldNotInstantiated)
from .fields import (BoolField, IntField, Int2Field, FloatField, Float2Field,
                     StringField, StringOptionField, IntOptionField)
from .form import (Form, Dialog, Widget)

with open(os.path.join(os.path.dirname(__file__), 'style.css')) as f:
    stylesheet = f.read()
