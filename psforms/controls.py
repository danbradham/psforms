# -*- coding: utf-8 -*-
'''
psforms.controls
================
Wraps standard PySide input widgets providing a unified api for getting and
setting their values. Each control implements :meth:`get_value` and
:meth:`set_value`. A required position argument ``value`` or
``values`` is used to set the default value of the control or in the case
of :class:`ComboBox` and :class:`IntComboBox` a sequence of items to add to
the wrapped QComboBox. In addition each control emits a Signal named `changed`
whenever the value is changed by user interaction.
'''
from PySide import QtGui, QtCore


class IconButton(QtGui.QPushButton):
    '''A button with an icon.

    :param icon: path to icon file or resource
    :param tip: tooltip text
    :param name: object name
    :param size: width, height tuple (default: (24, 24))
    '''

    def __init__(self, icon, tip, name, size=(24, 24), *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

        self.setObjectName(name)
        self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QtCore.QSize(*size))
        self.setSizePolicy(
            QtGui.QSizePolicy.Fixed,
            QtGui.QSizePolicy.Fixed)
        self.setFixedHeight(size[0])
        self.setFixedWidth(size[1])
        self.setToolTip(tip)


class Label(QtGui.QLabel):
    '''A label that emits a clicked signal on mouse press. Has the same
    signature as :class:`QtGui.QLabel`.'''

    clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.setFixedHeight(30)

    def mousePressEvent(self, event):
        self.clicked.emit()


class RightLabel(Label):
    '''Convenience right aligned Label'''

    def __init__(self, *args, **kwargs):
        super(RightLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


class LeftLabel(Label):
    '''Convenience left aligned Label'''

    def __init__(self, *args, **kwargs):
        super(LeftLabel, self).__init__(*args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)


class DoubleSpinBox(QtGui.QDoubleSpinBox):
    '''Wraps :class:`QtGui.QDoubleSpinBox`'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, *args, **kwargs):
        super(DoubleSpinBox, self).__init__(*args, **kwargs)
        self.nice_name = nice_name
        self.setFixedHeight(30)
        self.lineEdit().textEdited.connect(self.emit_changed)

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    def get_value(self):
        ''':return: Value of the underlying :class:`QtGui.QDoubleSpinBox`
        :rtype: float
        '''

        return self.value()

    def set_value(self, value):
        ''':param float value:'''

        self.setValue(value)


class TwinDoubleSpinBox(QtGui.QWidget):
    '''Composite widget with two :class:`DoubleSpinBox` s.'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, *args, **kwargs):
        super(TwinDoubleSpinBox, self).__init__(*args, **kwargs)
        self.nice_name = nice_name
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setFixedHeight(30)
        g = QtGui.QGridLayout()
        g.setSpacing(20)
        g.setContentsMargins(0, 0, 0, 0)
        self.setLayout(g)
        self.left_box = DoubleSpinBox('subcontrol')
        self.right_box = DoubleSpinBox('subcontrol')
        g.addWidget(self.left_box, 0, 0)
        g.addWidget(self.right_box, 0, 1)
        self.left_box.lineEdit().textEdited.connect(self.emit_changed)
        self.right_box.lineEdit().textEdited.connect(self.emit_changed)

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    def get_value(self):
        ''':returns: The value of each :class:`DoubleSpinBox`
        :rtype: tuple of two floats
        '''

        return self.left_box.get_value(), self.right_box.get_value()

    def set_value(self, value):
        ''':param value: A tuple including the values of both
        :class:`DoubleSpinBox` s
        '''

        self.left_box.setValue(value[0])
        self.right_box.setValue(value[1])


class SpinBox(QtGui.QSpinBox):
    '''Wraps :class:`QtGui.QSpinBox`'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, *args, **kwargs):
        super(SpinBox, self).__init__(*args, **kwargs)
        self.nice_name = nice_name
        self.setFixedHeight(30)
        self.lineEdit().textEdited.connect(self.emit_changed)

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    def get_value(self):
        ''':return: Value of the underlying :class:`QtGui.QSpinBox`
        :rtype: int
        '''

        return self.value()

    def set_value(self, value):
        ''':param int value:'''

        self.setValue(value)


class TwinSpinBox(QtGui.QWidget):
    '''Composite widget with two :class:`SpinBox` s.'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, *args, **kwargs):
        super(TwinSpinBox, self).__init__(*args, **kwargs)
        self.nice_name = nice_name
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setFixedHeight(30)
        g = QtGui.QGridLayout()
        g.setSpacing(20)
        g.setContentsMargins(0, 0, 0, 0)
        self.setLayout(g)
        self.left_box = SpinBox('subcontrol')
        self.right_box = SpinBox('subcontrol')
        g.addWidget(self.left_box, 0, 0)
        g.addWidget(self.right_box, 0, 1)
        self.left_box.lineEdit().textEdited.connect(self.emit_changed)
        self.right_box.lineEdit().textEdited.connect(self.emit_changed)

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    def get_value(self):
        ''':returns: The value of each :class:`QtGui.SpinBox`
        :rtype: tuple of two ints
        '''

        return self.left_box.get_value(), self.right_box.get_value()

    def set_value(self, value):
        ''':param value: A tuple including the values of both
        :class:`SpinBox` s
        '''

        self.left_box.setValue(value[0])
        self.right_box.setValue(value[1])


class ComboBox(QtGui.QComboBox):
    '''Wraps :class:`QtGui.QComboBox`'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, options, *args, **kwargs):
        super(ComboBox, self).__init__(*args, **kwargs)
        self.nice_name = nice_name
        self.setFixedHeight(30)
        self.addItems(options)
        self.activated.connect(self.emit_changed)

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    def get_data(self):
        return self.itemData(self.currentIndex(), QtCore.Qt.UserRole)

    def get_value(self):
        ''':return: Value of the underlying :class:`QtGui.QComboBox`
        :rtype: str
        '''

        return self.currentText()

    def set_value(self, value):
        ''':param str value:'''

        self.setCurrentIndex(self.findText(value))


class IntComboBox(QtGui.QComboBox):
    '''Wraps :class:`QtGui.QComboBox`. Assumes the items will be numeric'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, options, *args, **kwargs):
        super(IntComboBox, self).__init__(*args, **kwargs)
        self.nice_name = nice_name
        self.setFixedHeight(30)
        self.addItems([str(i) for i in options])
        self.activated.connect(self.emit_changed)

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    def get_value(self):
        ''':return: Value of the underlying :class:`QtGui.QComboBox`
        :rtype: int
        '''

        return int(self.currentText())

    def set_value(self, value):
        ''':param int value:'''

        self.setCurrentIndex(self.findText(str(value)))


class CheckBox(QtGui.QCheckBox):
    '''Wraps :class:`QtGui.QCheckBox`'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, *args, **kwargs):
        super(CheckBox, self).__init__(*args, **kwargs)
        self.nice_name = nice_name
        self.setFixedHeight(30)
        self.clicked.connect(self.emit_changed)

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    def get_value(self):
        ''':return: Value of the underlying :class:`QtGui.QCheckBox`
        :rtype: bool
        '''

        return self.isChecked()

    def set_value(self, value):
        ''':param bool value:'''

        self.setChecked(value)


class LineEdit(QtGui.QLineEdit):
    '''Wraps :class:`QtGui.QLineEdit`'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, *args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)
        self.nice_name = nice_name

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    def get_value(self):
        ''':return: Value of the underlying :class:`QtGui.QLineEdit`
        :rtype: str
        '''

        return self.text()

    def set_value(self, value):
        ''':param str value:'''

        self.setText(value)
