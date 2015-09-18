#!/usr/bin/env python
import sys
from PySide import QtGui
from psforms import stylesheet, controls, widgets
import signal


def vis_test_controls(labeled=True, label_on_top=True):

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)

    def control_as_dialog(control_cls):
        d = QtGui.QDialog()
        l = QtGui.QVBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(0)
        d.setLayout(l)
        control = control_cls(control_cls.__name__)
        if labeled:
            l.addWidget(widgets.Control(control, label_on_top))
        else:
            l.addWidget(control)
        return d


    for name in dir(controls):
        obj = getattr(controls, name)
        if hasattr(obj, 'is_control'):
            control_as_dialog(obj).exec_()


if __name__ == '__main__':

    args = sys.argv
    if len(args) > 1 and args[1] == '--visual':
        vis_test_controls()
