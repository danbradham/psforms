# -*- coding: utf-8 -*-
from .exc import FieldNotInstantiated
from . import controls
from .utils import Ordered
from copy import deepcopy


def get_key(key, from, **kwargs):
    value = None
    for d in dicts:
        value = d.get(value, None)
        if value:
            return value
    value = kwargs.get('default', None)
    if value:
        return value
    raise KeyError('{0} does not exist in {1}'.format(key, dicts))


class FieldType(Ordered):
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
    field_defaults = {'labeled': True, 'label_on_top': True, 'default':None}
    field_keys = ('labeled', 'label_on_top', 'default')

    def __init__(self, name, **kwargs):

        # Set instance attributes from field keys
        for key in self.field_keys:
            value = get_key(key, (kwargs, self.field_defaults), None)
            setattr(self, key, value)


        self.control_kwargs = {'nice_name': name}
        if control_defaults: # If the control has defaults, get em
            for key in self.control_defaults.iterkeys():
                value = get_key(key, (kwargs, self.control_defaults), None)
                if value:
                    self.control_kwargs[key] = value

    def __repr__(self):
        r = '<{}>(name={}, default={})'
        return r.format(self.__class__.__name__, self.name, self.default)

    def create(self):
        control = self.control_cls(**control_kwargs)
        if self.default:
            control.set_value(self.default)
        return control

def create_fieldtype(clsname, control_cls, control_defaults=None,
                     field_defaults=None, bases=(FieldType,)):
    '''Convenience function to create a new subclass of :class:`FieldType`.
    *control_defaults* are passed on to *control_cls*. *field_defaults* are
    used as the values of attributes on the returned :class:`FieldType`
    subclass. The keys for both control_defaults and field_defaults are looked
    up in __init__ kwargs param first.

    :param control_cls: PySide widget used to create the control.
    :param control_defaults: Default kwargs to pass to control_cls
    :param field_defaults: Default attr values (labeled, label_on_top, default)

    .. note::

        *control_cls* must  implement the :class:`ControlType` interface
    '''

    attrs = {
        'control_cls': control_cls,
        'control_defaults': control_defaults,
        'field_defaults': field_defaults or get_key('field_defaults', bases),
    }
    return type(clsname, bases, attrs)


ListField = create_fieldtype(
    'ListField',
    control_cls=controls.List,
)

BoolField = create_fieldtype(
    'BoolField',
    control_cls=controls.CheckBox,
    field_defaults={'label_on_top': False}
)

StringField = create_fieldtype(
    'StringField',

)
