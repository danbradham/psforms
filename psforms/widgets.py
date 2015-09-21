from PySide import QtGui, QtCore
import math
import os
from functools import partial
from . import resource


class CompositeFormWidget(QtGui.QWidget):
    '''Base Widget class, used to contain all field controls and groups.'''

    def __init__(self, layout_horizontal=False, parent=None):
        super(CompositeFormWidget, self).__init__(parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        if layout_horizontal:
            self.form_layout = QtGui.QHBoxLayout()
        else:
            self.form_layout = QtGui.QVBoxLayout()
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(0)

        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)

        self.forms = []
        self.header = None

    def __getattr__(self, attr):
        try:
            super(Form)
        for form in self.forms:
            try:
                return getattr(form, attr)
            except AttributeError:
                raise AttributeError('Widget has no attr: {}'.format(attr))

    def get_property(self, name):
        form_data = {}

        for form in self.forms:
            form_data.update(form.get_property(name))

        return form_data

    @property
    def valid(self):
        return all([form.valid for form in self.forms])

    def get_value(self):
        '''Get the values of all the controls'''

        data = {}

        for form in self.forms:
            data.update(form.get_value())

        return data

    def set_value(self, **data):
        '''Set the value of all the controls'''

        for form in self.forms:
            for name, control in controls:
                if name in data:
                    control.set_value(data[name])


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
        super(FormLayout, self).addWidget(widget, row, column)
        self.widgets.append(widget)


class FormWidget(QtGui.QWidget):

    def __init__(self, name, columns=1, layout_horizontal=False, parent=None):
        super(FormWidget, self).__init__(parent)

        self.name = name
        self.controls = []
        self.forms = []
        self.columns = columns
        self.parent = parent

        self.layout = QtGui.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        if layout_horizontal:
            self.form_layout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        else:
            self.form_layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(0)

        self.control_layout = ControlLayout(columns=columns)
        self.form_layout.addLayout(self.control_layout)
        self.layout.addLayout(self.form_layout)

        self.setProperty('form', True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def get_property(self, name):
        form_data = {}
        for name, control in self.controls.iteritems():
            form_data[name] = control.get_property(name)
        return form_data

    @property
    def valid(self):
        for name, control in self.controls.iteritems():
            self.validate_control(control)
        return all(self.get_property('valid').values())

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

    def validate_control(self, control):
        for v in control.validators:
            value = control.get_value()
            try:
                v(value)
            except ValidationError as err:
                control.set_property('valid', False)
        if not control.property('valid'):
            control.set_property('valid', True)

    def add_header(self, title, description=None, icon=None):
        self.header = Header(title, description, icon, self)
        self.layout.insertWidget(0, self.header)

    def add_form(self, name, form):
        self.form_layout.addWidget(form)
        self.forms.append(form)
        setattr(self, name, form)

    def add_control(self, name, control):
        count = len(self.controls)
        column = (count % self.columns)
        row = math.floor(count / self.columns)

        self.layout.addWidget(control.main_widget, row, column)
        self.controls[name] = control
        control.validate.connect(self.validate_control)

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
        if all(self.widget.valid):
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
