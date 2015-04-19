.. _guide:
.. currentmodule:: psforms

=====
Guide
=====
This guide will walk you through using psforms. Let's start by expanding on the example from the ReadMe.

::

    from psforms import (Form, IntField, StringField,
                         StringOptionField, BoolField)


    class MyForm(Form):
        '''My amazing form, useful in many scenarios.'''

        title = 'My Form'
        int_field = IntField('Integer Value')
        str_field = StringOptionField('String Value', options=['A', 'B', 'C'])
        bool_field = BoolField('Boolean Value')
        strb_field = StringField('String Value B')

The :class:`psforms.Form` is a factory for creating various types of forms.
:class:`psforms.Field` attributes are used to describe the input fields. :class:`psforms.Form` subclasses are only skeletons of a widget, waiting to be created. To create an actual form widget, use one of following methods, all of which start with the prefix **as_**.

Forms as Dialogs
================
::

    myform_dialog = MyForm.as_dialog()

    if myform_dialog.exec_():
        print dialog.get_value()

The :meth:`as_dialog` returns a :class:`psforms.Dialog` instance with the
fields specified in :class:`MyForm`. :class:`psforms.Dialog` accepts two
keyword arguments; columns and parent. :meth:`get_value` returns a :class:`FormData` including the names and values for all the fields in MyForm. :class:`FormData` supports both dictionary access and attribute access.

In this next example ``ParentWidget`` refers to a parent applications :class:`QtGui.QWidget` or :class:`QtGui.QMainWindow`.

::

    myform_dialog = MyForm.as_dialog(columns=2, parent=ParentWidget)

The previous examples create a modal dialog, which blocks all other PySide
widgets from receiving input until after the dialog is accepted or rejected.

Forms as Widgets and Groups
===========================
You can also get a Form as a mulit-column :class:`psforms.Widget` or
:class:`psforms.Group`.

::

    myform_widget = MyForm.as_widget(columns=2)
    myform_group = MyForm.as_group(columns=1, collapsable=True)

The above :class:`psforms.Widget` and :class:`psforms.Group` are derived from
a standard :class:`QtGui.QWidget` and a standard :class:`QtGui.QGroupBox`; therefore, they can be added to any PySide layout. The collapsable parameter
refers to whether or not the entire :class:`psforms.Group` can be collapsed. Both of these also have a :meth:`get_value` like the dialog above.

Getting the value of a control
==============================
All psform Field controls share the same api. You can use :meth:`set_value` to set them and :meth:`get_value` to retrieve them.

::

    myform_dialog.int_field.set_value(40)
    assert myform_dialog.int_field.get_value() == 40

All controls also have changed signal that are emitted whenever their values are modified by user interaction.
