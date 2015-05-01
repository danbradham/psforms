# -*- coding: utf-8 -*-
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from operator import attrgetter
from PySide import QtGui, QtCore

from .controls import LabeledControl
from .fields import Field
from .exc import FieldNotFound
from .widgets import Dialog, Widget, Header, Container
from .utils import Ordered, itemattrgetter


class Form(Ordered):

    title = None
    description = None
    icon = None
    header = False
    columns = 1
    labeled = True
    labels_on_top = True

    @classmethod
    def _fields(cls):
        '''Returns Field objects in sorted order'''

        cls_fields = []
        for name, attr in cls.__dict__.iteritems():
            if issubclass(attr.__class__, Field):
                cls_fields.append((name, attr))
        return sorted(cls_fields, key=itemattrgetter(1, '_order'))

    @classmethod
    def _forms(cls):
        '''Returns Form objects in sorted order'''

        cls_forms = []
        for name, attr in cls.__dict__.iteritems():
            if issubclass(attr.__class__, Form):
                cls_forms.append((name, attr))
        return sorted(cls_forms, key=itemattrgetter(1, '_order'))

    @classmethod
    def _create_controls(cls):
        '''Create and return controls from Field objects.'''

        controls = OrderedDict()

        for name, field in cls._fields():
            control = field.create()
            control.setObjectName(name)
            labeled = field.labeled or cls.labeled
            label_on_top = field.label_on_top or cls.labels_on_top
            if labeled:
                control = LabeledControl(control, label_on_top)
            controls[name] = control

        return controls

    @classmethod
    def create(cls, parent=None):
        '''Create a widget for this form using all Field attributes'''

        widget = Widget(cls.title, cls.columns, parent)
        controls = cls._create_controls()
        for name, control in controls.iteritems():
            widget.add_control(name, control)
        return widget

    @classmethod
    def as_widget(cls, parent=None):
        '''Get this form as a widget'''

        container = Container(parent)

        if cls.header:
            container.add_header(cls.title, cls.description, cls.icon)

        if cls._fields():
            widget = cls.create(parent)
            container.add_form(cls.title, widget)

        for name, form in cls._forms():
            container.add_form(name, form.create(container))

        return container

        return widget

    @classmethod
    def as_dialog(cls, parent=None):
        '''Get this form as a dialog'''

        dialog = Dialog(cls.as_widget(), parent=parent)
        dialog.setWindowTitle(cls.title)
        return dialog
