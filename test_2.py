import signal
import sys
import os
from pprint import pprint
from functools import partial
from PySide import QtGui, QtCore
from pslive import LiveLinker
from psforms import Form, stylesheet
from psforms.fields import *

signal.signal(signal.SIGINT, signal.SIG_DFL)


class SubFormA(Form):
    title = 'Sub Form A'
    labeled = True
    labels_on_top = True
    columns = 1

    int_field = IntField('Integer', range=(-100, 100), default=20)
    int2_field = Int2Field('Integer2')
    int_opt_field = IntOptionField('Integer3', options=[0, 1, 2])
    float_field = FloatField('Float', range=(10, 20))
    float2_field = Float2Field('Float2')
    str_field = StringOptionField('StringA', options=['A', 'B', 'C'])
    strb_field = StringField('StringB', default='B')


class SubFormB(Form):
    title = 'Sub Form B'
    labeled = True
    labels_on_top = False
    columns = 3

    bool_field = BoolField('Boolean', default=False)
    bool_fielda = BoolField('BooleanA', default=False)
    bool_fieldb = BoolField('BooleanB', default=False)
    bool_fieldc = BoolField('BooleanC', default=False)
    bool_fieldd = BoolField('BooleanD', default=False)
    bool_fielde = BoolField('BooleanE', default=False)
    bool_fieldf = BoolField('BooleanF', default=False)
    bool_fieldg = BoolField('BooleanG', default=False)
    bool_fieldh = BoolField('BooleanH', default=False)
    bool_fieldi = BoolField('BooleanI', default=False)
    bool_fieldj = BoolField('BooleanJ', default=False)
    bool_fieldk = BoolField('BooleanK', default=False)


class MyForm(Form):

    title = 'My Form'
    description = 'Why hello there, this is a test form'
    header = True

    subforma = SubFormA()
    subformb = SubFormB()


def form_accepted(form):
    print 'Form Accepted...\n'
    pprint(form.get_value())


def form_rejected(form):
    print 'Form Rejected...'


def print_values(form):
    pprint(form.get_value())


def test_stylesheet():

    app = QtGui.QApplication(sys.argv)

    myform = MyForm.as_widget()
    print_button = QtGui.QPushButton('print')
    print_button.clicked.connect(partial(print_values, myform))

    w = QtGui.QWidget()
    l = QtGui.QVBoxLayout()
    l.setContentsMargins(0, 0, 0, 0)
    f = QtGui.QHBoxLayout()
    f.setContentsMargins(20, 20, 20, 20)
    l.addWidget(myform)
    l.addLayout(f)
    f.addWidget(print_button)
    w.setLayout(l)
    w.show()

    w.setProperty('form', True) # Add form property to top-level widget
    w.setStyleSheet(stylesheet) # Apply psforms.stylesheet

    LiveLinker(path=os.path.abspath('psforms/style.css'), parent=w)

    sys.exit(app.exec_())


if __name__ == '__main__':
    test_stylesheet()
