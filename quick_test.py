import signal
import sys
from pprint import pprint
from functools import partial
from PySide import QtGui, QtCore
from psforms import Form, Field

signal.signal(signal.SIGINT, signal.SIG_DFL)


def print_values(form):
    pprint(form.get_value())

def test_widget():

    class MyForm(Form):
        title = 'My Form'
        int_field = Field('Integer Value', 20)
        str_field = Field('String Value', ['Item A', 'Item B', 'Item C'])
        bool_field = Field('Boolean Value', False)
        strb_field = Field('String Value B', '')

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


if __name__ == '__main__':
    test_widget()
