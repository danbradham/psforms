# -*- coding: utf-8 -*-
from .exc import FieldNotInstantiated
from . import controls
from . import widgets


class Counted(object):
    '''Maintains the order of creation for instances/subclasses'''

    _count = 0

    def __init__(self):
        Counted._count += 1
        self._order = self._count


class FieldGroup(Counted):
    '''Produces a group of fields arrayed in a number of columns.'''

    group_cls = widgets.Group

    def __init__(self, name, columns=1):
        super(FieldGroup, self).__init__()

        self.name = name
        self.columns = columns

    def create(self):
        group = self.group_cls(self.name, self.columns)
        return group


class Field(Counted):
    ''':class:`Form` calls the :meth:`create` to retrieve an appropriate
    control.

    :param name: Nice name of the field (str)
    :param labeled: Field Control has label (bool)
    :param label_on_top: Label appears on top of the field control (bool)
    :param group: FieldGroup the control belongs in
    :param on_left: Field control will appear on the left of group (bool)
    :param on_right: Field control will appear on the right of group (bool)
    :param default: Default value (str)
    '''

    control_cls = None

    def __init__(self, name, labeled=True, label_on_top=True,
                 group=None, on_left=None, on_right=None, default=None):
        super(Field, self).__init__()

        self.name = name
        self.labeled = labeled
        self.label_on_top = label_on_top
        self.group = group
        self.on_left = on_left
        self.on_right = on_right
        self.default = default

    def __repr__(self):
        r = '<{}>(name={}, default={})'
        return r.format(self.__class__.__name__, self.name, self.default)

    def create(self):
        control = self.control_cls(self.name)
        if self.default:
            control.set_value(self.default)
        return control


class BoolField(Field):
    '''Represented by a :class:`CheckBox` control.

    :param name: Nice name of the field (str)
    :param default: Default value (str)
    '''

    control_cls = controls.CheckBox

    def __init__(self, name, label_on_top=False, **kwargs):
        super(BoolField, self).__init__(name, label_on_top=label_on_top, **kwargs)

class StringField(Field):
    '''Represented by a :class:`LineEdit` control.

    :param name: Nice name of the field (str)
    :param default: Default value (str)
    '''

    control_cls = controls.LineEdit


class NumberField(Field):

    def __init__(self, name, range=None, **kwargs):

        super(NumberField, self).__init__(name, **kwargs)
        self.range = range

    def create(self):
        control = self.control_cls(self.name)
        if self.default:
            control.set_value(self.default)
        if self.range:
            control.setRange(*self.range)
        return control


class IntField(NumberField):
    '''Represented by a :class:`SpinBox` control.

    :param name: Nice name of the field (str)
    :param range: Tuple of minimum and maximum values
    :param default: Default value (int)
    '''

    control_cls = controls.SpinBox


class FloatField(NumberField):
    '''Represented by a :class:`DoubleSpinBox` control.

    :param name: Nice name of the field (str)
    :param range: Tuple of minimum and maximum values
    :param default: Default value (float)
    '''

    control_cls = controls.DoubleSpinBox


class Number2Field(Field):

    def __init__(self, name, range1=None, range2=None, **kwargs):
        super(Number2Field, self).__init__(name, **kwargs)
        self.range1 = range1
        self.range2 = range2

    def create(self):
        control = self.control_cls(self.name)
        if self.default:
            control.set_value(self.default)
        if self.range1:
            control.left_box.setRange(*self.range1)
        if self.range2:
            control.right_box.setRange(*self.range2)
        return control


class Int2Field(Number2Field):
    '''Represented by a :class:`TwinSpinBox` control.

    :param name: Nice name of the field (str)
    :param range1: Tuple of minimum and maximum values
    :param range2: Tuple of minimum and maximum values
    :param default: Default value (float, float)
    '''


    control_cls = controls.TwinSpinBox


class Float2Field(Number2Field):
    '''Represented by a :class:`TwinDoubleSpinBox` control.

    :param name: Nice name of the field (str)
    :param range1: Tuple of minimum and maximum values
    :param range2: Tuple of minimum and maximum values
    :param default: Default value (float)
    '''


    control_cls = controls.TwinDoubleSpinBox


class OptionField(Field):

    def __init__(self, name, options, **kwargs):
        super(OptionField, self).__init__(name, **kwargs)
        self.options = options

    def create(self):
        control = self.control_cls(self.name, self.options)
        if self.default:
            control.set_value(self.default)
        return control

class IntOptionField(OptionField):
    '''Represented by an :class:`IntComboBox` control.

    :param name: Nice name of the field (str)
    :param options: List of options
    :param default: Default value (int)
    '''

    control_cls = controls.IntComboBox

class StringOptionField(OptionField):
    '''Represented by an :class:`ComboBox` control.

    :param name: Nice name of the field (str)
    :param options: List of options
    :param default: Default value (str)
    '''

    control_cls = controls.ComboBox


