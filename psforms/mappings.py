# -*- coding: utf-8 -*-
'''
psforms.mappings
================
Mappings from standard python types to psforms.controls types.

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
 * list  -> controls.TwinSpinBox
 * tuple -> controls.TwinDoubleSpinBox
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
    list: controls.TwinSpinBox,
    tuple: controls.TwinDoubleSpinBox,
}
