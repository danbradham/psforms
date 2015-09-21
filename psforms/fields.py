# -*- coding: utf-8 -*-
from .exc import FieldNotInstantiated
from . import controls
from .utils import Ordered
from copy import deepcopy


def get_key(*args):
    '''Like dict.get but looks up keys in multiple dicts.

    :param key: Key to lookup
    :param dicts: Tuple of dicts to use in lookup
    :param default: If passed return this if lookup fails
    '''

    arglen = len(args)
    if not arglen in (2,3):
        raise ValueError('Must pass at least two args...key and (dicts...)')
    elif arglen == 2:
        key, dicts = args
    else:
        key, dicts, default = args

    value = None
    for d in dicts:
        value = d.get(key, None)
        if value:
            return value

    if 'default' in locals():
        return default

    raise KeyError('{0} does not exist in {1}'.format(key, dicts))


class FieldType(Ordered):
    ''':class:`Form` calls the :meth:`create` to retrieve an appropriate
    control.

    :param nice_name: Nice nice_name of the field (str)
    :param labeled: Field Control has label (bool)
        Overrides the parent Forms labeled attribute for this field only
    :param label_on_top: Label appears on top of the field control (bool)
        Overrides the parent Forms label_on_top attribute for this field only
    :param default: Default value (str)
    '''

    control_cls = None
    control_defaults = None
    field_defaults = {
        'labeled': True,
        'label_on_top': True,
        'default':None,
        'validators':None
    }
    field_keys = ('labeled', 'label_on_top', 'default', 'validators')

    def __init__(self, nice_name, **kwargs):
        super(FieldType, self).__init__()

        self.nice_name = nice_name
        self.control_kwargs = {'name': nice_name}
        # Set instance attributes from field keys
        for key in self.field_keys:
            value = get_key(key, (kwargs, self.field_defaults), None)
            self.control_kwargs[key] = value
            setattr(self, key, value)

        if self.control_defaults: # If the control has defaults, get em
            for key in self.control_defaults.iterkeys():
                value = get_key(key, (kwargs, self.control_defaults), None)
                if value:
                    self.control_kwargs[key] = value

    def __repr__(self):
        r = '<{}>(nice_name={}, default={})'
        return r.format(self.__class__.__name__, self.nice_name, self.default)

    def create(self):
        control = self.control_cls(**self.control_kwargs)
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

    bdicts = [b.__dict__ for b in bases]
    attrs = {
        'control_cls': control_cls,
        'control_defaults': control_defaults,
        'field_defaults': field_defaults or get_key('field_defaults', bdicts),
    }
    return type(clsname, bases, attrs)


ListField = create_fieldtype(
    'ListField',
    control_cls=controls.ListControl,
)

BoolField = create_fieldtype(
    'BoolField',
    control_cls=controls.BoolControl,
    field_defaults={'label_on_top': False}
)

StringField = create_fieldtype(
    'StringField',
    control_cls=controls.StringControl,
)

IntField = create_fieldtype(
    'IntField',
    control_cls=controls.IntControl,
    control_defaults={'range': None},
)

FloatField = create_fieldtype(
    'FloatField',
    control_cls=controls.FloatControl,
    control_defaults={'range': None},
)

Int2Field = create_fieldtype(
    'Int2Field',
    control_cls=controls.Int2Control,
    control_defaults={'range1': None, 'range2': None},
)

Float2Field = create_fieldtype(
    'Float2Field',
    control_cls=controls.Float2Control,
    control_defaults={'range1': None, 'range2': None},
)

IntOptionField = create_fieldtype(
    'IntOptionField',
    control_cls=controls.IntOptionControl,
    control_defaults={'options': None},
)

StringOptionField = create_fieldtype(
    'StringOptionField',
    control_cls=controls.StringOptionControl,
    control_defaults={'options': None},
)

FileField = create_fieldtype(
    'FileField',
    control_cls=controls.FileControl,
    control_defaults={'caption': None, 'filters': None},
)

FolderField = create_fieldtype(
    'FolderField',
    control_cls=controls.FolderControl,
    control_defaults={'caption': None, 'filters': None},
)

SaveFileField = create_fieldtype(
    'SaveFileField',
    control_cls=controls.SaveFileControl,
    control_defaults={'caption': None, 'filters': None},
)

ImageField = create_fieldtype(
    'ImageField',
    control_cls=controls.ImageControl,
)
