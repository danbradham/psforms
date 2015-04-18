# -*- coding: utf-8 -*-
from .exc import FieldNotInstantiated

class Field(object):

    _count = 0

    def __init__(self, name, default):
        #Maintain order of declaration
        self._count += 1
        self._order = self._count

        self.name = name
        self.default = default
        self.control = None
