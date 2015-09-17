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
import os
from PySide import QtGui, QtCore
from . import resource
from .widgets import ScalingImage


class LabeledControl(QtGui.QWidget):
    '''A composite widget with a label and a control.'''

    def __init__(self, control, label_on_top=True, parent=None):
        super(LabeledControl, self).__init__(parent=parent)

        self.control = control

        self.layout = QtGui.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        if label_on_top:
            self.label = Label(self.control.nice_name)
            self.layout.addWidget(self.control, 1, 0)
        else:
            self.label = RightLabel(self.control.nice_name)
            self.layout.setColumnStretch(1, 1)
            self.layout.addWidget(self.control, 0, 1)

        if isinstance(self.control, CheckBox):
            self.label.clicked.connect(self.control.toggle)
            self.label.setObjectName('clickable')

        self.label.setWordWrap(False)
        self.layout.addWidget(self.label, 0, 0)
        self.setLayout(self.layout)

    def __getattr__(self, attr):
        try:
            return getattr(self.control, attr)
        except AttributeError:
            raise AttributeError('Control has no attr: {}'.format(attr))


class IconButton(QtGui.QPushButton):
    '''A button with an icon.

    :param icon: path to icon file or resource
    :param tip: tooltip text
    :param name: object name
    :param size: width, height tuple (default: (24, 24))
    '''

    def __init__(self, icon, tip, name, size=(24, 24), *args, **kwargs):
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


class Label(QtGui.QLabel):
    '''A label that emits a clicked signal on mouse press. Has the same
    signature as :class:`QtGui.QLabel`.'''

    clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.setProperty('clickable', True)

    def mousePressEvent(self, event):
        self.clicked.emit()


class RightLabel(QtGui.QLabel):
    '''Convenience right aligned Label'''

    clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(RightLabel, self).__init__(*args, **kwargs)
        self.setProperty('clickable', True)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

    def mousePressEvent(self, event):
        self.clicked.emit()


class LeftLabel(QtGui.QLabel):
    '''Convenience left aligned Label'''

    clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(LeftLabel, self).__init__(*args, **kwargs)
        self.setProperty('clickable', True)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

    def mousePressEvent(self, event):
        self.clicked.emit()


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
        self.setFixedHeight(20)
        self.setFixedWidth(20)
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
        self.textChanged.connect(self.emit_changed)

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


class BaseBrowser(QtGui.QWidget):
    '''Composite :class:`QtGui.QLineEdit` with :class:`QtGui.QPushButton`
    for file browsing.
    '''

    browse_method = QtGui.QFileDialog.getOpenFileName
    changed = QtCore.Signal()

    def __init__(self, nice_name, caption=None, filters=None, *args, **kwargs):
        super(BaseBrowser, self).__init__(*args, **kwargs)
        self.nice_name = nice_name
        self.caption = caption or nice_name
        self.filters = filters or ["Any files (*)"]

        self.line = LineEdit(nice_name + '_line')
        self.line.changed.connect(self.emit_changed)
        self.get_value = self.line.get_value
        self.set_value = self.line.set_value
        self.button = IconButton(
            icon=':/icons/browse_hover',
            tip='File Browser',
            name='browse_button',
            )
        self.button.clicked.connect(self.browse)
        layout = QtGui.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setColumnStretch(0, 1)
        layout.addWidget(self.line, 0, 0)
        layout.addWidget(self.button, 0, 1)
        self.setLayout(layout)

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    @property
    def basedir(self):
        line_text = self.line.get_value()
        if line_text:
            line_dir = os.path.dirname(line_text)
            if os.path.exists(line_dir):
                return line_dir
        return ''

    def browse(self):
        value = self.browse_method(
            self,
            caption=self.caption,
            dir=self.basedir)
        if value:
            self.set_value(value[0])
            self.emit_changed()


class FileLine(BaseBrowser):
    '''Line Edit with file browsing button'''

    browse_method = QtGui.QFileDialog.getOpenFileName


class FolderLine(BaseBrowser):
    '''Line Edit with folder browsing button'''

    browse_method = QtGui.QFileDialog.getExistingDirectory


class SaveFileLine(BaseBrowser):
    '''Line Edit with save file browsing button'''

    browse_method = QtGui.QFileDialog.getSaveFileName


class ThumbnailLine(QtGui.QWidget):
    '''Image Browser'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, *args, **kwargs):
        super(ThumbnailLine, self).__init__(*args, **kwargs)
        self.nice_name = nice_name

        self.thumb = ScalingImage()
        self.file_line = FileLine(nice_name + '_line')
        self.file_line.changed.connect(self.emit_changed)

        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(self.thumb)
        layout.addWidget(self.file_line)
        self.setLayout(layout)

    def emit_changed(self, *args, **kwargs):
        self.thumb.set_image(self.file_line.get_value())
        self.changed.emit()

    def get_value(self):
        return self.file_line.get_value()

    def set_value(self, value):
        if os.path.exists(value):
            self.file_line.set_value(value)
        raise OSError('Path does not exist.')


class List(QtGui.QListWidget):
    '''Wraps :class:`QtGui.QListWidget`'''

    changed = QtCore.Signal()

    def __init__(self, nice_name, items=None, *args, **kwargs):
        super(Tree, self).__init__(*args, **kwargs)
        self.nice_name = nice_name
        if items:
            self.addItems(items)
        self.itemSelectionChanged.connect(self.emit_changed)

    def emit_changed(self, *args, **kwargs):
        self.changed.emit()

    def add_item(self, label, icon=None, data=None):
        item_widget = QtGui.QListWidgetItem()
        if icon:
            item_widget.setIcon(QtGui.QIcon(icon))
        if data:
            item_widget.setData(QtCore.Qt.UserRole, data)
        self.addItem(item_widget)

    def get_data(self):
        ''':return: Data for selected items in :class:`QtGui.QListWidget`
        :rtype: list'''
        items = self.selectedItems()
        items_data = []
        for item in items:
            items_data.append(item.data(QtCore.Qt.UserRole))
        return items_data

    def get_value(self):
        ''':return: Value of the underlying :class:`QtGui.QTreeWidget`
        :rtype: str'''

        items = self.selectedItems()
        item_values = []
        for item in items:
            item_values.append(item.text())
        return item_values


        '''Sets the selection of the list to the specified value, label or
        index'''

        if isinstance(value, (str, unicode)):
            items = self.findItems(value)
            if items:
                self.setCurrentItem(items[0])
        elif isinstance(value, int):
            self.setCurrentIndex(int)
