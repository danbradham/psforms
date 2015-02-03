# -*- coding: utf-8 -*-
'''
psforms.mappings
================
Mappings from standard python types to psform.controls types.

:attr standard_mapping: The default mapping::

    int   -> controls.SpinBox
    float -> controls.DoubleSpinBox
    bool  -> controls.CheckBox
    list  -> controls.ComboBox
    tuple -> controls.IntComboBox
    str   -> controls.LineEdit

:attr spin_mapping: Maps types to spinboxes::

    int   -> controls.SpinBox
    float -> controls.DoubleSpinBox
    list  -> controls.TwinDoubleSpinBox
    tuple -> controls.DoubleSpinBox

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


standard_mapping = {
    int: controls.SpinBox,
    float: controls.DoubleSpinBox,
    bool: controls.CheckBox,
    list: controls.ComboBox,
    tuple: controls.IntComboBox,
    str: controls.LineEdit,
}

spin_mapping = {
    int: controls.SpinBox,
    float: controls.DoubleSpinBox,
    list: controls.TwinDoubleSpinBox,
    tuple: controls.DoubleSpinBox,
}
