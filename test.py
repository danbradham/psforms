import signal
import sys
import os
from pprint import pprint
from functools import partial
from PySide import QtGui, QtCore
from pslive import LiveLinker
import psforms

signal.signal(signal.SIGINT, signal.SIG_DFL)


class MyForm(psforms.Form):
    title = 'My Form'
    bool_field = psforms.BoolField('Boolean', default=False)
    int_field = psforms.IntField('Integer', range=(-100, 100), default=20)
    int2_field = psforms.Int2Field('Integer2')
    int_opt_field = psforms.IntOptionField('Integer3', options=[0, 1, 2])
    float_field = psforms.FloatField('Float', range=(10, 20))
    float2_field = psforms.Float2Field('Float2')
    str_field = psforms.StringOptionField('StringA', options=['A', 'B', 'C'])
    strb_field = psforms.StringField('StringB', default='B')


def form_accepted(form):
    print 'Form Accepted...\n'
    pprint(form.get_value())


def form_rejected(form):
    print 'Form Rejected...'


def print_values(form):
    pprint(form.get_value())


def test_widget():

    app = QtGui.QApplication(sys.argv)

    myform = MyForm.as_widget()
    print_button = QtGui.QPushButton('print')
    print_button.clicked.connect(partial(print_values, myform))

    w = QtGui.QWidget()
    l = QtGui.QGridLayout()
    l.addWidget(myform, 0, 0, 1, 2)
    l.addWidget(print_button, 1, 1)
    w.setLayout(l)
    w.show()

    sys.exit(app.exec_())


def test_stylesheet():

    app = QtGui.QApplication(sys.argv)

    myform = MyForm.as_widget()
    print_button = QtGui.QPushButton('print')
    print_button.clicked.connect(partial(print_values, myform))

    w = QtGui.QWidget()
    l = QtGui.QGridLayout()
    l.addWidget(myform, 0, 0, 1, 2)
    l.addWidget(print_button, 1, 1)
    w.setLayout(l)
    w.show()

    w.setProperty('form', True) # Add form property to top-level widget
    w.setStyleSheet(psforms.stylesheet) # Apply psforms.stylesheet

    LiveLinker(path=os.path.abspath('psforms/style.css'), parent=w)

    sys.exit(app.exec_())


def test_widget_2column():

    app = QtGui.QApplication(sys.argv)

    myform = MyForm.as_widget(columns=2)
    print_button = QtGui.QPushButton('print')
    print_button.clicked.connect(partial(print_values, myform))

    w = QtGui.QWidget()
    l = QtGui.QGridLayout()
    l.addWidget(myform, 0, 0, 1, 2)
    l.addWidget(print_button, 1, 1)
    w.setLayout(l)
    w.show()

    sys.exit(app.exec_())


def test_widget_3column():

    app = QtGui.QApplication(sys.argv)

    myform = MyForm.as_widget(columns=3)
    print_button = QtGui.QPushButton('print')
    print_button.clicked.connect(partial(print_values, myform))

    w = QtGui.QWidget()
    l = QtGui.QGridLayout()
    l.addWidget(myform, 0, 0, 1, 2)
    l.addWidget(print_button, 1, 1)
    w.setLayout(l)
    w.show()

    sys.exit(app.exec_())


def test_group():

    app = QtGui.QApplication(sys.argv)

    myform = MyForm.as_group()
    print_button = QtGui.QPushButton('print')
    print_button.clicked.connect(partial(print_values, myform))

    w = QtGui.QWidget()
    w.setProperty('form', True)
    l = QtGui.QGridLayout()
    l.addWidget(myform, 0, 0, 1, 2)
    l.addWidget(print_button, 1, 1)
    w.setLayout(l)
    w.show()

    sys.exit(app.exec_())


def test_modal_dialog():

    app = QtGui.QApplication(sys.argv)

    myform = MyForm.as_dialog()
    if myform.exec_():
        pprint(myform.get_value())

    sys.exit(app.exec_())


def test_modeless_dialog():

    app = QtGui.QApplication(sys.argv)

    myform = MyForm.as_dialog()
    myform.accepted.connect(partial(form_accepted, myform))
    myform.rejected.connect(partial(form_rejected, myform))
    myform.setModal(True)
    myform.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    test_stylesheet()
