# -*- coding: utf-8 -*-
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from operator import attrgetter
from PySide import QtGui, QtCore

from .controls import LabeledControl
from .fields import Field, FieldGroup
from .exc import FieldNotFound
from .widgets import Dialog, Group, Header, Widget


class Form(object):

    title = None
    description = None
    icon = None
    header = False

    @classmethod
    def _fields(cls):
        cls_fields = []
        for name, attr in cls.__dict__.iteritems():
            if issubclass(attr.__class__, Field):
                cls_fields.append((name, attr))
        return sorted(cls_fields, key=lambda x: x[1]._order)

    @classmethod
    def _groups(cls):
        cls_groups = []
        for name, attr in cls.__dict__.iteritems():
            if issubclass(attr.__class__, FieldGroup):
                cls_groups.append((name, attr))
        return sorted(cls_groups, key=lambda x: x[1]._order)

    @classmethod
    def _create_groups(cls):
        groups = OrderedDict()

        field_groups = cls._groups()
        if not field_groups:
            groups['main'] = FieldGroup(name='main').create()

        for name, group in cls._groups():
            group = group.create()
            groups[name] = group

        return groups

    @classmethod
    def _create_controls(cls):
        controls = OrderedDict()

        for name, field in cls._fields():
            control = field.create()
            control.setObjectName(name)
            if field.labeled:
                control = LabeledControl(control, field.label_on_top)
            controls[name] = control

        return controls

    @classmethod
    def _create_widget(cls, parent=None):
        widget = Widget(parent=parent)

        if cls.header:
            widget.add_header(cls.title, cls.description, cls.icon)

        groups = cls._create_groups()
        controls = cls._create_controls()

        if len(groups) == 1:
            for name, control in controls.iteritems():
                groups['main'].add_control(name, control)
        else:
            groups_by_name = dict((g.name, g) for g in groups.values())
            for name, control in controls.iteritems():
                field = getattr(cls, name)
                group = groups_by_name[field.group.name]
                if field.group:
                    group.add_control(name, control)

        for name, group in groups.iteritems():
            widget.add_group(name, group)
        return widget

    @classmethod
    def as_widget(cls, parent=None):

        widget = cls._create_widget(parent=parent)
        return widget

    @classmethod
    def as_dialog(cls, parent=None):

        widget = cls._create_widget()
        dialog = Dialog(widget, parent=parent)
        dialog.setWindowTitle(cls.title)
        return dialog
