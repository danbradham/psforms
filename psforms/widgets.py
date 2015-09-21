from PySide import QtGui, QtCore
import math
import os
from functools import partial
from . import resource
from .exc import *


class ControlLayout(QtGui.QGridLayout):

    def __init__(self, columns=1, parent=None):
        super(ControlLayout, self).__init__(parent)

        self._columns = columns
        self.setContentsMargins(20, 20, 20, 20)
        self.setRowStretch(1000, 1)
        self.widgets = []

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value
        widgets = list(self.widgets)
        for w in widgets:
            self.takeWidget(w)
        for w in widgets:
            self.addWidget(w)

    @property
    def count(self):
        return len(self.widgets)

    def takeWidget(self, widget):
        if not widget in self.widgets:
            return None

        self.widgets.pop(self.widgets.index(widget))
        self.takeAt(self.indexOf(widget))
        return widget

    def addWidget(self, widget):
        count = self.count
        row = math.floor(count / self.columns)
        column = (count % self.columns)
        super(ControlLayout, self).addWidget(widget, row, column)
        self.widgets.append(widget)


class FormWidget(QtGui.QWidget):

    def __init__(self, name, columns=1, layout_horizontal=False, parent=None):
        super(FormWidget, self).__init__(parent)

        self.name = name
        self.controls = {}
        self.forms = {}
        self.parent = parent

        self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        if layout_horizontal:
            self.form_layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        else:
            self.form_layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(0)

        self.control_layout = ControlLayout(columns=columns)
        self.form_layout.addLayout(self.control_layout)
        self.layout.addLayout(self.form_layout)

        self.setProperty('form', True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    @property
    def valid(self):
        is_valid = []

        for name, control in self.controls.iteritems():
            control.validate()
            is_valid.append(control.valid)

        for name, form in self.forms.iteritems():
            is_valid.append(form.valid)

        return all(is_valid)

    def get_value(self, flatten=False):
        '''Get the value of this forms fields and subforms fields.

        :param flatten: If set to True, return a flattened dict
        '''

        form_data = {}
        for name, control in self.controls.iteritems():
            form_data[name] = control.get_value()

        for name, form in self.forms.iteritems():
            form_value = form.get_value(flatten=flatten)
            if flatten:
                form_data.update(form_value)
            else:
                form_data[name] = form_value

        return form_data

    def set_value(self, strict=True, **data):
        '''Set the value of all the forms subforms and fields. You can pass
        an additional keyword argument strict to False to ignore mismatched
        names and subforms.

        :param strict: raise exceptions for any invalid names in data
        :param data: Field data used to set the values of the form

        usage::

            myform.set_value(
                strict=True,
                **{
                    'strfield': 'ABCDEFG',
                    'intfield': 1,
                    'subform': {
                        'subform_strfield': 'BCDEFGH',
                        'subform_intfield': 2,}},
            )
        '''
        for name, value in data.iteritems():

            if isinstance(value, dict):
                try:
                    self.forms[name].set_value(**value)
                except KeyError:
                    if strict:
                        raise FormNotFound(name + ' does not exist')
                continue

            try:
                self.controls[name].set_value(value)
            except KeyError:
                if strict:
                    raise FieldNotFound(name + ' does not exist')

    def add_header(self, title, description=None, icon=None):
        '''Add a header'''

        self.header = Header(title, description, icon, self)
        self.layout.insertWidget(0, self.header)

    def add_form(self, name, form):
        '''Add a subform'''

        self.form_layout.addWidget(form)
        self.forms[name] = form
        setattr(self, name, form)

    def add_control(self, name, control):
        '''Add a control'''

        self.control_layout.addWidget(control.main_widget)
        self.controls[name] = control
        setattr(self, name, control)


class FormDialog(QtGui.QDialog):

    def __init__(self, widget, *args, **kwargs):
        super(FormDialog, self).__init__(*args, **kwargs)

        self.widget = widget
        self.cancel_button = QtGui.QPushButton('&cancel')
        self.accept_button = QtGui.QPushButton('&accept')
        self.cancel_button.clicked.connect(self.reject)
        self.accept_button.clicked.connect(self.on_accept)

        self.layout = QtGui.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setRowStretch(0, 1)
        self.setLayout(self.layout)

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.setContentsMargins(20, 20, 20, 20)
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.accept_button)

        self.layout.addWidget(self.widget, 0, 0)
        self.layout.addLayout(self.button_layout, 1, 0)

    def __getattr__(self, attr):
        try:
            return getattr(self.widget, attr)
        except AttributeError:
            raise AttributeError('FormDialog has no attr: {}'.format(attr))

    def on_accept(self):
        if self.widget.valid:
            self.accept()
        return


class Header(QtGui.QWidget):

    def __init__(self, title, description=None, icon=None, parent=None):
        super(Header, self).__init__(parent)

        self.grid = QtGui.QGridLayout()

        self.setLayout(self.grid)

        self.title = QtGui.QLabel(title)
        self.title.setProperty('title', True)
        if description:
            self.descr = QtGui.QLabel(description)
            self.descr.setProperty('description', True)
            self.descr.setAlignment(QtCore.Qt.AlignCenter)
        if icon:
            self.icon = QtGui.QLabel()
            self.icon.setPixmap(icon)
            self.grid.addWidget(self.icon, 0, 0)
            self.grid.addWidget(self.title, 0, 1)
            self.grid.addWidget(self.descr, 1, 0, 1, 2)
        else:
            self.grid.addWidget(self.title, 0, 0)
            self.grid.addWidget(self.descr, 1, 0)
            self.title.setAlignment(QtCore.Qt.AlignCenter)

        self.setProperty('header', True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self._mouse_button = None
        self._mouse_last_pos = None

    def mousePressEvent(self, event):
        self._mouse_button = event.button()
        super(Header, self).mousePressEvent(event)
        self._window = self.window()

    def mouseMoveEvent(self, event):
        '''Click + Dragging moves window'''

        if self._mouse_button == QtCore.Qt.LeftButton:
            if self._mouse_last_pos:

                p = self._window.pos()
                v = event.globalPos() - self._mouse_last_pos
                self._window.move(p + v)

            self._mouse_last_pos = event.globalPos()

        super(Header, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._mouse_button = None
        self._mouse_last_pos = None
        self._window = None
        super(Header, self).mouseReleaseEvent(event)


class ScalingImage(QtGui.QLabel):

    __images = {}

    def __init__(self, image=None, parent=None):
        super(ScalingImage, self).__init__(parent)
        self.images = self.__images
        if not image:
            image = ':/images/noimg'
        self.set_image(image)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Expanding)

    def set_image(self, image):
        if not image in self.images:
            if not isinstance(image, QtGui.QImage):
                if not QtCore.QFile.exists(image):
                    return
                self.img = QtGui.QImage(image)
            self.images[image] = self.img
        else:
            self.img = self.images[image]

        self.setMinimumSize(227, 128)
        self.scale_pixmap()
        self.repaint()

    def scale_pixmap(self):
        scaled_image = self.img.scaled(
            self.width(),
            self.height(),
            QtCore.Qt.KeepAspectRatioByExpanding,
            QtCore.Qt.FastTransformation)
        self.pixmap = QtGui.QPixmap(scaled_image)

    def resizeEvent(self, event):
        self.do_resize = True
        super(ScalingImage, self).resizeEvent(event)

    def paintEvent(self, event):
        if self.do_resize:
            self.scale_pixmap()
            self.do_resize = False

        offsetX = -((self.pixmap.width() - self.width())*0.5)
        offsetY = -((self.pixmap.height() - self.height())*0.5)
        painter = QtGui.QPainter(self)
        painter.drawPixmap(offsetX, offsetY, self.pixmap)


class IconButton(QtGui.QPushButton):
    '''A button with an icon.

    :param icon: path to icon file or resource
    :param tip: tooltip text
    :param name: object name
    :param size: width, height tuple (default: (30, 30))
    '''

    def __init__(self, icon, tip, name, size=(30, 30), *args, **kwargs):
        super(IconButton, self).__init__(*args, **kwargs)

        self.setObjectName(name)
        self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QtCore.QSize(*size))
        self.setSizePolicy(
            QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        self.setFixedHeight(size[0])
        self.setFixedWidth(size[1])
        self.setToolTip(tip)
