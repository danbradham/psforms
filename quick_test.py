import signal
import sys
from pprint import pprint
from functools import partial
from PySide import QtGui, QtCore
import psforms

signal.signal(signal.SIGINT, signal.SIG_DFL)


class MyForm(psforms.Form):
    title = 'My Form'
    int_field = psforms.IntField('Integer', range=(-100, 100), default=20)
    str_field = psforms.StringOptionField('StringA', options=['A', 'B', 'C'])
    bool_field = psforms.BoolField('Boolean', default=False)
    strb_field = psforms.StringField('StringB', default='B')
    int2_field = psforms.Int2Field('Integer2')
    float2_field = psforms.Float2Field('Float2')
    int_opt_field = psforms.IntOptionField('Integer3', options=[0, 1, 2])


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
    test_modal_dialog()
