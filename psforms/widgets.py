from PySide import QtGui, QtCore
import math
from . import controls


class Container(QtGui.QWidget):
    '''Base Widget class, used to contain all field controls and groups.'''

    def __init__(self, parent=None):
        super(Container, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.forms = []
        self.header = None

    def __getattr__(self, attr):
        for form in self.forms:
            try:
                return getattr(form, attr)
            except AttributeError:
                raise AttributeError('Widget has no attr: {}'.format(attr))

    def add_header(self, title, description=None, icon=None):
        header = Header(title, description, icon, self)
        self.layout.addWidget(header)

    def add_form(self, name, form):
        self.layout.addWidget(form)
        self.forms.append(form)
        setattr(self, name, form)

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


class Widget(QtGui.QWidget):

    def __init__(self, name, columns=1, parent=None):
        super(Widget, self).__init__(parent)

        self.name = name
        self.controls = {}
        self.columns = columns
        self.parent = parent

        self.layout = QtGui.QGridLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setRowStretch(1000, 1)
        self.setLayout(self.layout)

        self.setProperty('form', True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

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
        count = len(self.controls)
        column = (count % self.columns)
        row = math.floor(count / self.columns)

        self.layout.addWidget(control, row, column)
        self.controls[name] = control

        setattr(self, name, control)


class Dialog(QtGui.QDialog):

    def __init__(self, widget, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)

        self.widget = widget
        self.cancel_button = QtGui.QPushButton('&cancel')
        self.accept_button = QtGui.QPushButton('&accept')
        self.cancel_button.clicked.connect(self.reject)
        self.accept_button.clicked.connect(self.accept)

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
            raise AttributeError('Dialog has no attr: {}'.format(attr))


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
