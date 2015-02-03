# -*- coding: utf-8 -*-
'''
psforms.mappings
================
Mappings from standard python types to psform.controls types.

:attr:`STANDARD`
----------------
The default mapping

 * int   -> controls.SpinBox
 * float -> controls.DoubleSpinBox
 * bool  -> controls.CheckBox
 * list  -> controls.ComboBox
 * tuple -> controls.IntComboBox
 * str   -> controls.LineEdit

:attr:`SPIN`
------------
Maps types to spinboxes

 * int   -> controls.SpinBox
 * float -> controls.DoubleSpinBox
 * list  -> controls.TwinDoubleSpinBox
 * tuple -> controls.DoubleSpinBox

These are used with the :class:`ControlFactory` s to produce controls from a
dictionary like this one::

    controls = {
        'MySpinBox': ('My Nice SpinBox', 20),
        'MyComboBox': ('My Nice ComboBox', ['Item A', 'Item B', 'Item C']),
        'MyCheckBox': ('My Nice CheckBox', False),
        'MyLineEdit': ('My Nice LineEdit', ''),
    }
'''

from . import controls


STANDARD = {
    int: controls.SpinBox,
    float: controls.DoubleSpinBox,
    bool: controls.CheckBox,
    list: controls.ComboBox,
    tuple: controls.IntComboBox,
    str: controls.LineEdit,
}

SPIN = {
    int: controls.SpinBox,
    float: controls.DoubleSpinBox,
    list: controls.TwinDoubleSpinBox,
    tuple: controls.DoubleSpinBox,
}
