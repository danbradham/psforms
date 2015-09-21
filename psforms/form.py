# -*- coding: utf-8 -*-
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from operator import attrgetter
from PySide import QtGui, QtCore

from .fields import FieldType
from .exc import FieldNotFound
from .widgets import FormDialog, FormWidget, Header
from .utils import Ordered, itemattrgetter


class FormMetaData(object):

    defaults = dict(
        title='No Title',
        description='No Description',
        icon=None,
        header=False,
        columns=1,
        label=True,
        labels_on_top=True,
        layout_horizontal=False,
    )

    def __init__(self, **kwargs):
        self.__dict__.update(self.defaults)
        self.__dict__.update(kwargs)


class Form(Ordered):

    meta = FormMetaData()

    @classmethod
    def fields(cls):
        '''Returns FieldType objects in sorted order'''

        cls_fields = []
        for name, attr in cls.__dict__.iteritems():
            if issubclass(attr.__class__, FieldType):
                cls_fields.append((name, attr))
        return sorted(cls_fields, key=itemattrgetter(1, '_order'))

    @classmethod
    def forms(cls):
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

        fields = cls.fields()

        # Get the width of the maximum length label
        _max_label = max([y.nice_name for x, y in fields], key=len)
        _label = QtGui.QLabel(_max_label)
        max_width = _label.sizeHint().width() + 10

        for name, field in cls.fields():
            control = field.create()
            control.setObjectName(name)
            labeled = field.labeled or cls.meta.labeled
            label_on_top = field.label_on_top or cls.meta.labels_on_top
            control.label.setFixedWidth(max_width)
            controls[name] = control

        return controls

    @classmethod
    def as_widget(cls, parent=None):
        '''Get this form as a widget'''

        form_widget = FormWidget(
            cls.meta.title,
            cls.meta.columns,
            cls.meta.layout_horizontal,
            parent=parent)

        if cls.meta.header:
            form_widget.add_header(
                cls.meta.title,
                cls.meta.description,
                cls.meta.icon
            )

        if cls.fields():
            controls = cls._create_controls()
            for name, control in controls.iteritems():
                form_widget.add_control(name, control)

        for name, form in cls.forms():
            form_widget.add_form(name, form.as_widget(form_widget))

        return form_widget

    @classmethod
    def as_dialog(cls, frameless=False, dim=False, parent=None):
        '''Get this form as a dialog'''

        dialog = FormDialog(cls.as_widget(), parent=parent)
        dialog.setWindowTitle(cls.meta.title)
        window_flags = QtCore.Qt.WindowStaysOnTopHint
        if frameless:
            window_flags |= QtCore.Qt.FramelessWindowHint
        dialog.setWindowFlags(window_flags)

        if dim: # Dim all monitors when showing the dialog
            def _bg_widgets():
                qapp = QtGui.QApplication.instance()
                desktop = qapp.desktop()
                screens = desktop.screenCount()
                widgets = []

                for i in xrange(screens):
                    geo = desktop.screenGeometry(i)
                    w = QtGui.QWidget()
                    w.setGeometry(geo)
                    w.setStyleSheet('QWidget {background:black}')
                    w.setWindowOpacity(0.3)
                    widgets.append(w)

                def show():
                    for w in widgets:
                        w.show()
                def hide():
                    for w in widgets:
                        w.hide()
                return show, hide

            old_exec = dialog.exec_
            old_show = dialog.show
            def _exec_(*args, **kwargs):
                bgshow, bghide = _bg_widgets()
                bgshow()
                result = old_exec(*args, **kwargs)
                bghide()
                return result

            def _show(*args, **kwargs):
                bgshow, bghide = _bg_widgets()
                bgshow()
                result = old_show(*args, **kwargs)
                bghide()
                return result

            dialog.exec_ = _exec_
            dialog.show = _show

        return dialog
