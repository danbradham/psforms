# -*- coding: utf-8 -*-
import math
from operator import attrgetter
from PySide import QtGui, QtCore

from .controls import RightLabel, CheckBox
from .mappings import STANDARD
from .field import Field
from .exc import FieldNotFound


class FormWidget(QtGui.QWidget):

    def __init__(self, controls, columns=1, labeled=True, parent=None):
        super(FormWidget, self).__init__(parent)

        self.setObjectName('Form')
        self.controls = controls
        self.columns = columns
        self.labeled = labeled
        self.parent = parent
        self._count = 0

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.setRowStretch(1000, 1)
        self.layout.setContentsMargins(20, 20, 20, 20)

        for name, control in self.controls.iteritems():
            self.add_control(name, control)

    def get_value(self):
        form_data = {}
        for name, control in self.controls.iteritems():
            form_data[name] = control.get_value()

        return form_data

    def set_value(self, **data):
        for name, value in data.iteritems():
            try:
                self.controls[name].set_value(value)
            except KeyError:
                raise FieldNotFound(name + ' does not exist')

    def add_control(self, name, control):
        column = (self._count % self.columns) * 2
        row = math.floor(self._count / self.columns)

        label = RightLabel(control.nice_name)
        label.setObjectName(name + '_label')
        self.layout.addWidget(label, row, column)
        self.layout.addWidget(control, row, column + 1)

        if isinstance(control, CheckBox):
            label.clicked.connect(control.toggle)
            label.setObjectName('clickable')

        setattr(self, name, control)

        self._count += 1


class Form(object):

    title = ''
    mapping = STANDARD

    @classmethod
    def _fields(cls):
        cls_fields = []
        for name, attr in cls.__dict__.iteritems():
            if isinstance(attr, Field):
                cls_fields.append((name, attr))

        return sorted(cls_fields, key=lambda x: x[1]._order)

    @classmethod
    def _create_controls(cls):
        controls = {}
        print cls._fields()

        for name, field in cls._fields():
            typ = type(field.default)
            control = cls.mapping[typ](field.name, field.default)
            control.setObjectName(name)
            controls[name] = control

        return controls

    @classmethod
    def as_widget(cls, columns=1, labeled=True, parent=None):

        widget = FormWidget(cls._create_controls())
        return widget
