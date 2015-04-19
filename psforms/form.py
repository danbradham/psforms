# -*- coding: utf-8 -*-
import math
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from operator import attrgetter
from PySide import QtGui, QtCore

from .controls import RightLabel, CheckBox
from .fields import Field
from .exc import FieldNotFound


class FormData(dict):
    '''Dictionary in which attribute lookup is redirected to itself access.
    Simplest possible implementation. Returned by get_value calls to
    :class:`Dialog`, :class:`Widget` and :class:`GroupBox`
    '''

    __getattr__ = dict.__getitem__


class Widget(QtGui.QWidget):

    def __init__(self, controls, columns=1, labeled=True, parent=None):
        super(Widget, self).__init__(parent)

        self.setProperty('form', True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
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
        form_data = FormData()
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


class Dialog(QtGui.QDialog):

    def __init__(self, widget, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)

        self.widget = widget
        self.cancel_button = QtGui.QPushButton('&cancel')
        self.accept_button = QtGui.QPushButton('&accept')
        self.cancel_button.clicked.connect(self.reject)
        self.accept_button.clicked.connect(self.accept)

        self.layout = QtGui.QGridLayout()
        self.layout.setRowStretch(0, 1)
        self.layout.setColumnStretch(0, 1)
        self.setLayout(self.layout)

        self.layout.addWidget(self.widget, 0, 0, 1, 3)
        self.layout.addWidget(self.cancel_button, 1, 1)
        self.layout.addWidget(self.accept_button, 1, 2)

    def __getattr__(self, attr):
        try:
            return getattr(self.widget, attr)
        except AttributeError:
            raise AttributeError('Dialog has no attr: {}'.format(attr))


class Group(QtGui.QGroupBox):

    def __init__(self, title, widget, parent=None):
        super(Group, self).__init__(title, parent=parent)

        self.widget = widget

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.setRowStretch(1000, 1)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.addWidget(self.widget, 0, 0)

        self.unfolded = True
        self.setProperty('unfolded', True)
        self.setCheckable(True)
        self.setChecked(True)
        self.clicked.connect(self.fold)

    def __getattr__(self, attr):
        try:
            return getattr(self.widget, attr)
        except AttributeError:
            raise AttributeError('Dialog has no attr: {}'.format(attr))

    def fold(self):
        '''Toggle visibility for all widgets'''
        self.setChecked(True)
        self.unfolded = not self.unfolded

        num_children = self.layout.count()
        for i in xrange(num_children):
            c = self.layout.itemAt(i).widget()
            c.setVisible(self.unfolded)

        for name, control in self.widget.controls.iteritems():
            control.setEnabled(True) # Controls are always enabled

        self.setProperty('unfolded', not self.property('unfolded'))
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()


class Form(object):

    title = None

    @classmethod
    def _fields(cls):
        cls_fields = []
        for name, attr in cls.__dict__.iteritems():
            if issubclass(attr.__class__, Field):
                cls_fields.append((name, attr))
        return sorted(cls_fields, key=lambda x: x[1]._order)

    @classmethod
    def _create_controls(cls):
        controls = OrderedDict()

        for name, field in cls._fields():
            typ = type(field.default)
            control = field.create()
            control.setObjectName(name)
            controls[name] = control

        return controls

    @classmethod
    def as_widget(cls, columns=1, labeled=True, parent=None):

        widget = Widget(
            controls=cls._create_controls(),
            columns=columns,
            labeled=labeled,
            parent=parent)
        return widget

    @classmethod
    def as_dialog(cls, columns=1, labeled=True, parent=None):

        widget = Widget(
            controls=cls._create_controls(),
            columns=columns,
            labeled=labeled,
            parent=parent)
        dialog = Dialog(widget)
        dialog.setWindowTitle(cls.title)
        return dialog

    @classmethod
    def as_group(cls, columns=1, labeled=True, parent=None):

        widget = Widget(
            controls=cls._create_controls(),
            columns=columns,
            labeled=labeled,
            parent=parent)
        group = Group(title=cls.title, widget=widget, parent=parent)
        return group
