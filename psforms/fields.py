# -*- coding: utf-8 -*-
from .exc import FieldNotInstantiated
from . import controls
from .utils import Ordered
from copy import deepcopy


class Field(Ordered):
    ''':class:`Form` calls the :meth:`create` to retrieve an appropriate
    control.

    :param name: Nice name of the field (str)
    :param labeled: Field Control has label (bool)
        Overrides the parent Forms labeled attribute for this field only
    :param label_on_top: Label appears on top of the field control (bool)
        Overrides the parent Forms label_on_top attribute for this field only
    :param default: Default value (str)
    '''

    control_cls = None
    control_defaults = None
    field_defaults = None

    def __init__(self, name, labeled=None, label_on_top=None, default=None):
        super(Field, self).__init__()

        self.name = name
        self.labeled = field_defaults.get('labeled', labeled)
        self.label_on_top = field_defaults.get('label_on_top', label_on_top)
        self.default = field_defaults.get('default', default)

    def __repr__(self):
        r = '<{}>(name={}, default={})'
        return r.format(self.__class__.__name__, self.name, self.default)

    def create(self):
        control_kwargs = deepcopy(control_defaults)
        control_kwargs['nice_name'] = self.name
        control = self.control_cls(**control_kwargs)
        if self.default:
            control.set_value(self.default)
        return control


# def create_field(clsname, control_cls, control_defaults, field_defaults):





class ListField(Field):
    '''Represented by a :class:`List` control

    :param name: Nice name of field (str)
    :param default: Default value (list of strings)
    '''

    control_cls = controls.List


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


class BrowseField(Field):

    def __init__(self, name, caption=None, filters=None, **kwargs):
        super(BrowseField, self).__init__(name, **kwargs)
        self.caption = caption
        self.filters = filters

    def create(self):
        control = self.control_cls(self.name, self.caption, self.filters)
        if self.default:
            control.set_value(self.default)
        return control


class FileField(BrowseField):
    '''Represented by a :class:`FileLine` control

    :param name: Nice name of the field (str)
    :param default: Default value (str)'''

    control_cls = controls.FileLine


class FolderField(BrowseField):
    '''Represented by a :class:`FolderLine` control

    :param name: Nice name of the field (str)
    :param default: Default value (str)'''

    control_cls = controls.FolderLine


class SaveFileField(BrowseField):
    '''Represented by a :class:`FolderLine` control

    :param name: Nice name of the field (str)
    :param default: Default value (str)'''

    control_cls = controls.SaveFileLine



class ImageField(Field):
    '''Represented by an :class:`ThumbnailLine` control

    :param name: Nice name of the field (str)
    :param default: Default value (str filepath)
    '''

    control_cls = controls.ThumbnailLine

