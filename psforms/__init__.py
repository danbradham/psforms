# -*- coding: utf-8 -*-

__title__ = 'psforms'
__author__ = 'Dan Bradham'
__email__ = 'danielbradham@gmail.com'
__url__ = 'http://github.com/danbradham/psforms.git'
__version__ = '0.2.0'
__license__ = 'MIT'
__description__ = 'Hassle free PySide forms.'

import os

from . import resource
from . import controls
from .exc import (FormNotInstantiated, FieldNotFound, FieldNotInstantiated)
from .fields import (BoolField, IntField, Int2Field, FloatField, Float2Field,
                     StringField, StringOptionField, IntOptionField)
from .form import (Form, Dialog, Widget)

with open(os.path.join(os.path.dirname(__file__), 'style.css')) as f:
    stylesheet = f.read()
